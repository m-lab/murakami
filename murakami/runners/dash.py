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
        device_id=None, device_metadata1=None, device_metadata2=None):
        super().__init__(
            title="DASH",
            description="The Neubot DASH network test.",
            config=config,
            data_cb=data_cb,
            device_id=device_id,
            device_metadata1=device_metadata1,
            device_metadata2=device_metadata2,
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
