from datetime import datetime
import logging
import pkg_resources
import shutil

from webthing import Action, Property, Thing, Value

from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class Murakami(Thing):
    def __init__(self):
        self._runners = {}

        Thing.__init__(
            self,
            id_="https://github.com/throneless-tech/murakami",
            title="Murakami",
            type_=[],
            description="The M-Lab Murakami network measurement tap.",
        )

        # Load test runners
        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading test runner %s", entry_point.name)
            rconfig = {}
            self._runners[entry_point.name] = entry_point.load()(
                config=rconfig)

        for name, runner in self._runners.items():
            self.add_property(
                Property(
                    self,
                    runner.title + "on",
                    Value(
                        runner.config.get("enabled", True),
                        lambda onoff: runner.config.update(enabled=onoff),
                    ),
                    metadata={
                        "@type": "OnOffProperty",
                        "id": runner.title + "on",
                        "title": runner.title,
                        "type": "boolean",
                        "description": runner.description,
                    },
                ))

            self.add_available_event(
                "error",
                {
                    "description": "There was an error running the tests",
                    "type": "string",
                    "unit": "error",
                },
            )

            def _start_test(self):
                raise RunnerError(self.name, "No _start_test() function implemented.")

            def start_test(self):
                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                data = self._runners[r]._start_test()
                if self._runners[r]._data_cb is not None:
                    self._runners[r]._data_cb(test_name=self._runners[r].title, data=data, timestamp=timestamp)
                return data

            def _stop_test(self):
                logger.debug("No special handling needed for stopping runner %s",
                             self.title)

            def stop_test(self):
                return self._runners[r]._stop_test()

            def _teardown(self):
                logger.debug("No special teardown needed for runner %s", self._runners[r].title)

            def teardown(self):
                return self._runners[r]._teardown()

            self._runners[r].start_test = start_test(self)
            self._runners[r].stop_test = stop_test(self)
            self._runners[r]._teardown = _teardown(self)
            self._runners[r].teardown = teardown(self)
