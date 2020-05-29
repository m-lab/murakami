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
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="DASH",
            description="The Neubot DASH network test.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id,
        )

    @staticmethod
    def _start_test():
        logger.info("Starting DASH test...")
        if shutil.which("dash-client") is not None:
            output = subprocess.run(["dash-client"],
                                    check=True,
                                    text=True,
                                    capture_output=True)
            logger.info("Dash test complete.")
            # TODO: write parser. Only print the last line for now.
            return output.stdout.splitlines()[-1]
        else:
            raise RunnerError(
                "dash",
                "Executable dash-client does not exist, please install DASH.")
