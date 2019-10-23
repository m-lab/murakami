import logging
import shutil
import subprocess
import uuid

import jsonlines
from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class RunDash(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.debug("Running %s test via Webthings.", self.thing.title)
        results = self.thing.start_test()
        self.thing.set_property("results", results)

class DashClient():
    """Run Dash tests."""
    def __init__(self, config=None, data_cb=None):
        self.attype="DashRunner"
        self.id_="https://github.com/neubot/dash"
        self.title="DASH"
        self.type=["Test"]
        self.description="The Neubot DASH network test."
        self.config=config
        self.data_cb=data_cb
        self.action = RunDash()

    def _start_test(self):
        if shutil.which("dash-client") is not None:
            output = subprocess.run(["dash-client"],
                                    check=True,
                                    text=True,
                                    capture_output=True)
            reader = jsonlines.Reader(output.stdout.splitlines())
        else:
            raise RunnerError(
                "dash",
                "Executable dash-client does not exist, please install DASH.")
        return [*reader.iter()]
