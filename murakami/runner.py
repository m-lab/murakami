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
            description="The M-Lab Murakami network measurement tap."
        )

        # Load test runners
        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading test runner %s", entry_point.name)
            rconfig = {}
            self._runners[entry_point.name] = entry_point.load()(
                config=rconfig)

        for r in self._runners:
            self.add_property(
                Property(
                    self,
                    r,
                    Value([]),
                    metadata={
                        "@type": self._runners[r].attype,
                        "id": self._runners[r].id_,
                        "title": self._runners[r].title,
                        "type": self._runners[r].type,
                        "description": self._runners[r].description,
                        "config": self._runners[r].config,
                        "data_cb": self._runners[r].data_cb,
                    },
                )
            )

            self.add_available_action("run", {
                "title": "run_" + self._runners[r].title,
                "description": "Run tests",
                "input": {
                    "type": "object",
                    "required": [self._runners[r].title],
                    "properties": {
                        "test": {
                            "type": ["Test"],

                        }
                    }
                }
            }, self._runners[r].action)

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
        data = self._start_test()
        if self._data_cb is not None:
            self._data_cb(test_name=self.title, data=data, timestamp=timestamp)
        return data

    def _stop_test(self):
        logger.debug("No special handling needed for stopping runner %s",
                     self.title)

    def stop_test(self):
        return self._stop_test()

    def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.title)

    def teardown(self):
        return self._teardown()
