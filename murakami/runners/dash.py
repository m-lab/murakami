import logging
import shutil
import subprocess
import uuid

import jsonlines

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class DashClient(MurakamiRunner):
    """Run Dash tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            title="DASH",
            description="The Neubot DASH network test.",
            config=config,
            data_cb=data_cb,
        )

    @staticmethod
    def _start_test():
        logger.info("Starting DASH test...")
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
        return [*reader.iter(skip_empty=True, skip_invalid=True)]
