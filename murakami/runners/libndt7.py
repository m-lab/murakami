import logging
import shutil
import subprocess
import uuid

import jsonlines

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class LibndtClient(MurakamiRunner):
    """Run LibNDT tests."""
    def __init__(self, config=None, data_cb=None):
        print(config)
        super().__init__(
            title="ndt7",
            description="The Network Diagnostic Tool v7 test.",
            config=config,
            data_cb=data_cb,
        )

    def _start_test(self):
        logger.info("Starting NDT7 test...")
        if shutil.which("libndt-client") is not None:
            cmdargs = [
                "libndt-client",
                "--download",
                "--upload",
                "--json",
                "--websocket",
                "--tls",
                "--ndt7",
                "--batch",
            ]

            if "host" in self._config:
                # If a host has been specified, also default to -insecure
                # as it will likely use a self-signed certificate.
                cmdargs.append("--insecure")
                cmdargs.append(self._config['host'])

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
                "libndt",
                "Executable libndt-client does not exist, please install libndt.",
            )
        return [*reader.iter(skip_empty=True, skip_invalid=True)]
