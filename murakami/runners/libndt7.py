import logging
import shutil
import subprocess
import uuid

import jsonlines
from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class RunLibndt(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.info("Performing ndt7 test")
        self.thing.start_test()


class LibndtClient(MurakamiRunner):
    """Run LibNDT tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(name="ndt7", config=config, data_cb=data_cb)

        self._thing = Thing(
            "urn:dev:ops:libndt-client",
            "LibNDT Client",
            ["OnOffSwitch", "Client"],
            "A client running LibNDT tests",
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
            RunLibndt,
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
        if shutil.which("libndt-client") is not None:
            output = subprocess.run(
                [
                    "libndt-client",
                    "--download",
                    "--upload",
                    "--lookup-policy=closest",
                    "--json",
                    "--websocket",
                    "--tls",
                    "--ndt7",
                    "--batch",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            reader = jsonlines.Reader(output.stdout.splitlines())
        else:
            raise RunnerError(
                "libndt",
                "Executable libndt-client does not exist, please install libndt.",
            )
        return [*reader.iter(skip_empty=True)]
