import logging
import shutil
import subprocess
import uuid

import jsonlines

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt5Client(MurakamiRunner):
    """Run NDT5 test."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(
            title="ndt5",
            description="The Network Diagnostic Tool v5 test.",
            config=config,
            data_cb=data_cb,
        )

    def _start_test(self):
        logger.info("Starting NDT5 test...")
        if shutil.which("ndt5-client") is not None:
            cmdargs = [
                "ndt5-client",
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
            logger.info("NDT5 test complete.")
        else:
            raise RunnerError(
                "ndt5-client",
                "Executable ndt5-client does not exist, please install ndt5-client-go.",
            )
        return [*reader.iter(skip_empty=True, skip_invalid=True)]
