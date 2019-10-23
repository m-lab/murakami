import datetime
import logging
import random
import time
import pkg_resources

from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.triggers.base import BaseTrigger
from tornado import gen
from tornado.ioloop import IOLoop
from webthing import WebThingServer, SingleThing

import murakami.defaults as defaults
import murakami.utils as utils

from murakami.runner import Murakami

logger = logging.getLogger(__name__)

_SHUTDOWN_TIMEOUT = 30


class RandomTrigger(BaseTrigger):
    def __init__(self, *args, **kwargs):
        self._tests_per_day = kwargs.pop("tests_per_day",
                                         defaults.TESTS_PER_DAY)
        self._immediate = kwargs.pop("immediate", False)

    def get_next_fire_time(self, previous_fire_time, now):
        sleeptime = random.expovariate(
            1.0 /
            (datetime.timedelta(days=1).total_seconds() / self._tests_per_day))
        if not previous_fire_time:
            logger.debug("Not previously fired before")
            if self._immediate:
                return now
            previous_fire_time = now

        return previous_fire_time + datetime.timedelta(seconds=sleeptime)


class MurakamiServer:
    def __init__(
            self,
            port=defaults.HTTP_PORT,
            hostname=None,
            ssl_options=None,
            additional_routes=None,
            base_path="",
            tests_per_day=defaults.TESTS_PER_DAY,
            immediate=False,
            webthings=False,
            location=None,
            network_type=None,
            connection_type=None,
            config=None,
    ):
        self._runners = {}
        self._exporters = {}

        self._scheduler = None
        self._server = None

        self._port = port
        self._hostname = hostname
        self._ssl_options = ssl_options
        self._additional_routes = additional_routes
        self._base_path = base_path
        self._tests_per_day = tests_per_day
        self._immediate = immediate
        self._webthings = webthings
        self._location = location
        self._network_type = network_type
        self._connection_type = connection_type
        self._config = config

    def _call_runners(self):
        for r in self._runners:
            # Only run test if enabled
            enabled = True
            if "tests" in self._config:
                if r in self._config["tests"]:
                    rconfig = self._config["tests"][r]
                    if "enabled" in rconfig:
                        enabled = utils.is_enabled(rconfig["enabled"])
            if enabled:
                logger.info("Running test: %s", r)
                try:
                    self._runners[r].start_test
                except Exception as exc:
                    logger.error("Failed to run test %s: %s", r, str(exc))
            else:
                logging.debug("Test runner %s disabled, skipping.", r)

    def _call_exporters(self, test_name="", data="", timestamp=None):
        for e in self._exporters.values():
            logger.info("Running exporter %s for test %s", e.name, test_name)
            try:
                e.push(test_name, data, timestamp)
            except Exception as exc:
                logger.error("Failed to run exporter %s: %s", e.name, str(exc))

    def _load_runners(self):
        thing = Murakami()
        trigger = RandomTrigger(tests_per_day=self._tests_per_day,
                                immediate=self._immediate)

        # Load test runners
        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading test runner %s", entry_point.name)
            rconfig = {}
            self._runners[entry_point.name] = entry_point.load()(
                config=rconfig, data_cb=self._call_exporters)

        # Start webthings server if enabled
        if self._webthings:
            self._server = WebThingServer(
                SingleThing(thing),
                port=self._port,
                hostname=self._hostname,
                ssl_options=self._ssl_options,
                additional_routes=self._additional_routes,
                base_path=self._base_path,
            )

        # Start test scheduler if enabled
        if self._tests_per_day > 0:
            self._scheduler = TornadoScheduler()
            self._scheduler.add_job(self._call_runners,
                                    id="runners",
                                    name="Test Runners",
                                    trigger=trigger)

    def _load_exporters(self):
        self._exporters = {}
        # Check if exporters are enabled and load them.
        if "exporters" in self._config:
            exporters = pkg_resources.get_entry_map("murakami",
                                                    group="murakami.exporters")
            for name, entry in self._config["exporters"].items():
                logging.debug("Loading exporter %s", name)
                enabled = True
                if "enabled" in entry:
                    enabled = utils.is_enabled(entry["enabled"])
                if enabled:
                    if "type" in entry:
                        if entry["type"] in exporters:
                            self._exporters[name] = exporters[
                                entry["type"]].load()(
                                    name=name,
                                    location=self._location,
                                    network_type=self._network_type,
                                    connection_type=self._connection_type,
                                    config=entry,
                                )
                        else:
                            logging.error(
                                "No available exporter type %s, skipping.",
                                entry["type"],
                            )
                    else:
                        logging.error(
                            "No type defined for exporter %s, skipping.", name)
                else:
                    logging.debug("Exporter %s disabled, skipping.", name)

    def start(self):
        logger.info("Starting Murakami services.")
        self._load_runners()
        self._load_exporters()

        if self._scheduler is not None:
            logger.info("Starting the job scheduler.")
            self._scheduler.start()
        if self._server is not None:
            logger.info("Starting the WebThing server.")
            self._server.start()
        if self._scheduler is not None and self._server is None:
            IOLoop.current().start()

    def stop(self):
        logger.info("Stopping Murakami services.")

        IOLoop.current().stop()

        if self._scheduler is not None:
            logger.info("Stopping the job scheduler.")
            self._scheduler.shutdown()
        if self._server is not None:
            logger.info("Stopping the WebThing server.")
            self._server.stop()

        logger.info("Cleaning up test runners.")

        for r in self._runners:
            self._runners[r].stop_test()
            self._runners[r].teardown()

    @gen.coroutine
    def reload(self, signum, frame, **kwargs):
        local_args = dict(locals())
        logger.info("Reloading Murakami services...")
        for key, _ in local_args.items():
            if key in kwargs:
                setattr(self, key, kwargs[key])
        yield IOLoop.current().add_callback_from_signal(self.stop)
        self.start()
