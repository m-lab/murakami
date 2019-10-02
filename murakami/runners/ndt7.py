import logging
import os
import shutil
import uuid

from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class RunNdt7(Action):
    def __init__(self, thing, input_):

        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.info("Performing NDT7 test")
        self.thing.start_test()


class Ndt7Client(MurakamiRunner):
    """Run NDT7 tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(name="ndt7", config=config, data_cb=data_cb)

        self._thing = Thing(
            "urn:dev:ops:ndt7-client",
            "NDT7 Client",
            ["OnOffSwitch", "Client"],
            "A client running NDT7 tests",
        )

        self._thing.add_property(
            Property(
                self,
                "on",
                Value(True, lambda v: print("On-State is now", v)),
                metadata={
                    "@type": "OnOffProperty",
                    "title": "On/Off",
                    "type": "boolean",
                    "description": "Whether the client is running",
                },
            ))

        self._thing.add_available_action(
            "run",
            {
                "title": "Run",
                "description": "Run tests",
                "input": {
                    "type": "object",
                    "required": ["download", "upload"],
                    "properties": {
                        "download": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                        "upload": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                    },
                },
            },
            RunNdt7,
        )

        self._thing.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def _start_test(self):
        if shutil.which("ndt7-client") is not None:
            os.system("ndt7-client")
        else:
            raise RunnerError(
                "ndt7",
                "Executable does not exist, please install ndt7-client.")
