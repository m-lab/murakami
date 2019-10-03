import logging
import shutil
import subprocess
import uuid

import jsonlines
from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class RunSpeedtest(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.info("Performing Speeedtest.net test")
        self.thing.start_test()


class SpeedtestClient(MurakamiRunner):
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(name="speedtest", config=config, data_cb=data_cb)

        self.thing = Thing(
            "urn:dev:ops:speedtest-client",
            "Speedtest Client",
            ["OnOffSwitch", "Client"],
            "A client running Speedtest.net tests",
        )

        self.thing.add_property(
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

        self.thing.add_available_action(
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
            RunSpeedtest,
        )

        self.thing.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def _start_test(self):
        if shutil.which("speedtest-cli") is not None:
            output = subprocess.run(["speedtest-cli", "--json"],
                                    check=True,
                                    text=True,
                                    capture_output=True)
            reader = jsonlines.Reader(output.stdout.splitlines())
        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest-cli.")
        return [*reader.iter()]
