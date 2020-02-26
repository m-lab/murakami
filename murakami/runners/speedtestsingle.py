import logging
import shutil
import subprocess
import uuid
import datetime
import json

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner
from murakami.runners.speedtest import SpeedtestClient

logger = logging.getLogger(__name__)


class SpeedtestSingleClient(MurakamiRunner):
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None):
        super().__init__(
            title="Speedtest-cli-single-stream",
            description="The Speedtest.net test (https://github.com/sivel/speedtest-cli).",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type
        )

    def _start_test(self):
        logger.info("Starting Speedtest single stream test...")
        if shutil.which("speedtest-cli") is not None:
            starttime = datetime.datetime.utcnow()
            output = subprocess.run(["speedtest-cli",
                                     "--single", "--json"],
                                    text=True,
                                    capture_output=True)
            endtime = datetime.datetime.utcnow()

            murakami_output = {
                'TestName': "speedtest-cli-single-stream",
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'MurakamiLocation': self._location,
                'MurakamiConnectionType': self._connection_type,
                'MurakamiNetworkType': self._network_type
            }

            murakami_output.update(SpeedtestClient._parse_summary(output))
            return json.dumps(murakami_output)
        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest-cli.")
