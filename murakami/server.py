"""
This module contains the core of Murakami. It includes the plugin and
WebThingServer loading code.
"""

import datetime
import logging
import random
import pkg_resources

from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.triggers.base import BaseTrigger
from tornado.ioloop import IOLoop
from tornado import gen
from webthing import WebThingServer, SingleThing

import murakami.defaults as defaults
from murakami.thing import MurakamiThing
import murakami.utils as utils

_logger = logging.getLogger(__name__)

_SHUTDOWN_TIMEOUT = 30


class RandomTrigger(BaseTrigger):
    """
    An implementation of apscheduler's BaseTrigger to schedule tests in an
    exponential distribution.
    """
    def __init__(self, *args, **kwargs):
        self._tests_per_day = kwargs.pop("tests_per_day",
                                         defaults.TESTS_PER_DAY)
        self._immediate = kwargs.pop("immediate", False)

    def get_next_fire_time(self, previous_fire_time, now):
        sleeptime = random.expovariate(
            1.0 /
            (datetime.timedelta(days=1).total_seconds() / self._tests_per_day))
        if not previous_fire_time:
            _logger.debug("Not previously fired before")
            if self._immediate:
                return now
            previous_fire_time = now

        return previous_fire_time + datetime.timedelta(seconds=sleeptime)


class MurakamiServer:
    """
    *MurakamiServer* is responsible for loading all test runner and result
    exporter plugins, as well as managing the main eventloop and loading
    WebThings if desired.

    ####Keyword arguments:
    * `port`: port that WebThingsServer listens on
    * `hostname`: this WebThingServer's hostname
    * `ssl_options`: any TLS options to supply to WebThingServer
    * `additonal_routes`: routes to add to the WebThingServer
    * `base_path`: path to add to URL where we're listening in case we're
    behind a proxy
    * `tests_per_day`: number of tests to run in a day
    * `location`: string describing physical location of this device
    * `network_type`: string describing the network this device is connected to
    * `connection_type`: string describing type of connection this device is
    using
    """
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
            device_id=None,
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
        self._device_id = device_id
        self._config = config

    def _call_runners(self):
        for r in self._runners.values():
            _logger.info("Running test: %s", r.title)
            try:
                r.start_test()
            except Exception as exc:
                _logger.error("Failed to run test %s: %s", r.title, str(exc))

    def _call_exporters(self, test_name="", data="", timestamp=None):
        for e in self._exporters.values():
            _logger.info("Running exporter %s for test %s", e.name, test_name)
            try:
                e.push(test_name, data, timestamp)
            except Exception as exc:
                _logger.error("Failed to run exporter %s: %s", e.name,
                              str(exc))

    def _load_runners(self):
        trigger = RandomTrigger(tests_per_day=self._tests_per_day,
                                immediate=self._immediate)

        # Load test runners
        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading test runner %s", entry_point.name)
            if "tests" not in self._config:
                self._config["tests"] = {}
            if entry_point.name not in self._config["tests"]:
                self._config["tests"][entry_point.name] = {"enabled": False}
            self._runners[entry_point.name] = entry_point.load()(
                config=self._config["tests"][entry_point.name],
                data_cb=self._call_exporters,
                location=self._location,
                network_type=self._network_type,
                connection_type=self._connection_type,
                device_id=self._device_id,
            )

        # Start webthings server if enabled
        if self._webthings:
            self._server = WebThingServer(
                SingleThing(MurakamiThing(self._runners.values())),
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
        """Start MurakamiServer, including WebThingServer if directed."""
        _logger.info("Starting Murakami services.")
        self._load_runners()
        self._load_exporters()

        if self._scheduler is not None:
            _logger.info("Starting the job scheduler.")
            self._scheduler.start()
        if self._server is not None:
            _logger.info("Starting the WebThing server.")
            self._server.start()
        if self._scheduler is not None and self._server is None:
            IOLoop.current().start()

    def stop(self):
        """Stop MurakamiServer."""
        _logger.info("Stopping Murakami services.")

        IOLoop.current().stop()

        if self._scheduler is not None:
            _logger.info("Stopping the job scheduler.")
            self._scheduler.shutdown()
        if self._server is not None:
            _logger.info("Stopping the WebThing server.")
            self._server.stop()

        _logger.info("Cleaning up test runners.")

        for r in self._runners:
            self._runners[r].stop_test()
            self._runners[r].teardown()

    @gen.coroutine
    def reload(self, signum, frame, **kwargs):
        """Reload MurakamiServer, to be called as an event handler."""
        local_args = dict(locals())
        _logger.info("Reloading Murakami services...")
        for key, _ in local_args.items():
            if key in kwargs:
                setattr(self, key, kwargs[key])
        yield IOLoop.current().add_callback_from_signal(self.stop)
        self.start()
