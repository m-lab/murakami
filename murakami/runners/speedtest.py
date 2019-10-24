import logging
import shutil
import subprocess
import uuid

import jsonlines

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class SpeedtestClient(MurakamiRunner):
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            title="Speedtest.net",
            description="The Speedtest.net tool.",
            config=config,
            data_cb=data_cb,
        )

    @staticmethod
    def _start_test():
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
        return [
            *reader.iter(skip_empty=True, skip_invalid=True)
        ]
