import datetime
import logging
import random
import pkg_resources
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.triggers.base import BaseTrigger
from webthing import WebThingServer, MultipleThings

import murakami.defaults as defaults

logger = logging.getLogger(__name__)


def is_enabled(toggle):
    return str(toggle).lower() in ["true", "yes", "1", "y"]


class RandomTrigger(BaseTrigger):
    def __init__(self, *args, **kwargs):
        super().__init__()
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
            config=None,
    ):
        self.runners = {}
        self.exporters = {}

        self.scheduler = TornadoScheduler()
        trigger = RandomTrigger(tests_per_day=tests_per_day,
                                immediate=immediate)

        # Check if exporters are enabled and load them.
        if "exporters" in config:
            exporters = pkg_resources.get_entry_map("murakami",
                                                    group="murakami.exporters")
            for name, entry in config["exporters"].items():
                logging.debug("Loading exporter %s", name)
                enabled = False
                if "enabled" in entry:
                    enabled = is_enabled(entry["enabled"])
                if enabled:
                    if "type" in entry:
                        if entry["type"] in exporters:
                            self.exporters[name] = exporters[
                                entry["type"]].load()(name=name, config=entry)
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

        def call_exporters(test_name="", data="", timestamp=None):
            for e in self.exporters.values():
                e.push(test_name, data, timestamp)

        def call_runners():
            for r in self.runners.values():
                logger.info("Running test: %s", r.name)
                r.start_test()

        # Check if test runners are enabled and load them.
        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading test runner %s", entry_point.name)
            rconfig = {}
            enabled = True
            if "tests" in config:
                if entry_point.name in config["tests"]:
                    rconfig = config["tests"][entry_point.name]
                    if "enabled" in rconfig:
                        enabled = is_enabled(rconfig["enabled"])
            if enabled:
                self.runners[entry_point.name] = entry_point.load()(
                    config=rconfig, data_cb=call_exporters)
            else:
                logging.debug("Test runner %s disabled, skipping.",
                              entry_point.name)
        if tests_per_day > 0:
            self.scheduler.add_job(call_runners,
                                   id="runners",
                                   name="runners",
                                   trigger=trigger)

        self.server = WebThingServer(
            MultipleThings([r.thing for r in self.runners.values()],
                           "Murakami"),
            port=port,
            hostname=hostname,
            ssl_options=ssl_options,
            additional_routes=additional_routes,
            base_path=base_path,
        )

    def start(self):
        logger.info("Starting the job scheduler.")
        self.scheduler.start()
        logger.info("Starting the WebThing server.")
        self.server.start()

    def stop(self):
        logger.info("Stopping the job scheduler.")
        self.scheduler.shutdown()
        logger.info("Stopping the WebThing server.")
        self.server.stop()
