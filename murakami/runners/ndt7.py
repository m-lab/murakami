import logging
import shutil
import subprocess
import uuid

import jsonlines

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt7Client(MurakamiRunner):
    """Run ndt7 test."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            title="ndt7",
            description="The Network Diagnostic Tool v7 test.",
            config=config,
            data_cb=data_cb,
        )

    def _start_test(self):
        logger.info("Starting ndt7 test...")
        if shutil.which("ndt7-client") is not None:
            cmdargs = [
                "ndt7-client",
                "-format=json",
                "-quiet"
            ]

            if "host" in self._config:
                cmdargs.append(self._config['host'])
                insecure = self._config.get('insecure', True)
                if insecure:
                    cmdargs.append('--insecure')

            output = subprocess.run(
                cmdargs,
                check=True,
                text=True,
                capture_output=True,
            )
            reader = jsonlines.Reader(output.stdout.splitlines())
            logger.info("NDT7 test complete.")
        else:
            raise RunnerError(
                "ndt7-client",
                "Executable ndt7-client does not exist, please install ndt7-client-go.",
            )
        return [*reader.iter(skip_empty=True, skip_invalid=True)]
