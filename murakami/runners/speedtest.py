import logging
import shutil
import subprocess
import uuid

import jsonlines
from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class RunSpeedtest(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.debug("Running %s test via Webthings.", self.thing.title)
        results = self.thing.start_test()
        self.thing.set_property("results", results)


class SpeedtestClient():
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None):
        self.attype="SpeedtestRunner"
        self.id_="https://github.com/sivel/speedtest-cli"
        self.title="Speedtest.net"
        self.type=["Test"]
        self.description="The Speedtest.net tool."
        self.config=config
        self.data_cb=data_cb
        self.action = RunSpeedtest

    def _start_test(self):
        logger.info("Starting Speedtest test...")
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
