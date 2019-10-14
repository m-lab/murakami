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
        logger.debug("Running %s test via Webthings.", self.thing.title)
        results = self.thing.start_test()
        self.thing.set_property("results", results)


class LibndtClient(MurakamiRunner):
    """Run LibNDT tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            id_="https://www.measurementlab.net/tests/ndt/ndt7",
            title="ndt7",
            type_=["Test"],
            description="The Network Diagnostic Tool v7 test.",
            config=config,
            data_cb=data_cb,
        )

        self.add_property(
            Property(
                self,
                "results",
                Value([]),
                metadata={
                    "@type": "MurakamiJsonl",
                    "title": "Results",
                    "type": "array",
                    "description": "The results of the last test",
                },
            ))

        self.add_available_action("run", {
            "title": "Run",
            "description": "Run tests"
        }, RunLibndt)

        self.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def _start_test(self):
        logger.info("Starting ndt7 test...")
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
