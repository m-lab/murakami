import logging
import shutil
import subprocess
import uuid

import jsonlines
from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class RunLibndt(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.debug("Running %s test via Webthings.", self.thing.title)
        results = self.thing.start_test()
        self.thing.set_property("results", results)


class LibndtClient():
    """Run LibNDT tests."""
    def __init__(self, config=None, data_cb=None):
        self.attype="LibNDT5Runner"
        self.id_="https://www.measurementlab.net/tests/ndt/ndt5"
        self.title="ndt5"
        self.type=["Test"]
        self.description="The Network Diagnostic Tool v5 test."
        self.config=config
        self.data_cb=data_cb
        self.action = RunLibndt

    def _start_test(self):
        logger.info("Starting NDT5 test...")
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
        return [*reader.iter(allow_none=True, skip_empty=True, skip_invalid=True)]
