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
        logger.debug("Running %s test via Webthings.", self.thing.title)
        results = self.thing.start_test()
        self.thing.set_property("results", results)


class SpeedtestClient(MurakamiRunner):
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            id_="https://github.com/sivel/speedtest-cli",
            title="Speedtest.net",
            type_=["Test"],
            description="The Speedtest.net tool.",
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
        }, RunSpeedtest)

        self.add_available_event(
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
