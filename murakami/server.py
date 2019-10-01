import datetime
import logging
import pkg_resources
import random
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.triggers.base import BaseTrigger
from webthing import WebThingServer, MultipleThings

logger = logging.getLogger(__name__)


class RandomTrigger(BaseTrigger):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._expected_sleep_seconds = kwargs.pop("expected_sleep_seconds",
                                                  12 * 60 * 60)

    def get_next_fire_time(self, previous_fire_time, now):
        sleeptime = random.expovariate(1.0 / self._expected_sleep_seconds)
        if not previous_fire_time:
            previous_fire_time = now
        return previous_fire_time + datetime.timedelta(seconds=sleeptime)


class MurakamiServer:
    def __init__(
            self,
            port=80,
            hostname=None,
            ssl_options=None,
            additional_routes=None,
            base_path="",
            tests_per_day=2,
            expected_sleep_seconds=12 * 60 * 60,
            config=None,
    ):
        self.runners = {}

        self.scheduler = TornadoScheduler()
        trigger = RandomTrigger(expected_sleep_seconds=expected_sleep_seconds)

        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading plugin %s", entry_point.name)
            rconfig = {}
            enabled = True
            if "tests" in config:
                if entry_point.name in config["tests"]:
                    rconfig = config["tests"][entry_point.name]
                    if "enabled" in rconfig:
                        enabled = str(rconfig["enabled"]).lower() in [
                            "true",
                            "yes",
                            "1",
                            "y",
                        ]
            if enabled:
                self.runners[entry_point.name] = entry_point.load()(
                    config=rconfig)
                if tests_per_day > 0:
                    self.scheduler.add_job(
                        self.runners[entry_point.name].start_test,
                        id=entry_point.name,
                        name=entry_point.name,
                        trigger=trigger,
                    )
            else:
                logging.debug("Plugin %s disabled, skipping.",
                              entry_point.name)

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
