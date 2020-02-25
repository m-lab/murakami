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
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None):
        super().__init__(
            title="Speedtest-cli-multi-stream",
            description="The Speedtest.net multi-stream test (https://github.com/sivel/speedtest-cli).",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type
        )

    @staticmethod
    def _start_test():
        logger.info("Starting Speedtest multi-stream test...")
        if shutil.which("speedtest-cli") is not None:
            output = subprocess.run(["speedtest-cli", "--json"],
                                    check=True,
                                    text=True,
                                    capture_output=True)

            logger.info("Speedtest multi-stream test complete.")

            # TODO: write parser. Only print the last line for now.
            return output.stdout.splitlines()[-1]
        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest-cli.")