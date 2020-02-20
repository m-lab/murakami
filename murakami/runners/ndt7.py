import logging
import shutil
import subprocess
import uuid
import json
import datetime 

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt7Client(MurakamiRunner):
    """Run ndt7 test."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None):
        super().__init__(
            title="ndt7",
            description="The Network Diagnostic Tool v7 test.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type
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

            starttime = datetime.datetime.utcnow()
            output = subprocess.run(
                cmdargs,
                check=True,
                text=True,
                capture_output=True,
            )
            endtime = datetime.datetime.utcnow()

            murakami_output = {
                'TestName': "ndt7",
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'MurakamiLocation': self._location,
                'MurakamiConnectionType': self._connection_type,
                'MurakamiNetworkType': self._network_type
            }

             # Parse ndt7 summary.
            summary = {}
            try:
                summary = json.loads(output.stdout)
            except json.JSONDecodeError:
                raise RunnerError(
                    'ndt7-client',
                    'ndt7-client did not return a valid JSON summary.'
                )

            if output.returncode == 0:
                logger.info("ndt7 test completed successfully.")
                print("Summary: {}".format(summary))
                murakami_output['ServerName'] = summary['Server']
                murakami_output['ClientIP'] = summary['Client']
                murakami_output['DownloadValue'] = summary['Download']['Value']
                murakami_output['DownloadUnit'] = summary['Download']['Unit']
                murakami_output['DownloadError'] = None
                murakami_output['DownloadRetransValue'] = summary['DownloadRetrans']['Value']
                murakami_output['DownloadRetransUnit'] = summary['DownloadRetrans']['Unit']
                murakami_output['UploadValue'] = summary['Upload']['Value']
                murakami_output['UploadUnit'] = summary['Upload']['Unit']
                murakami_output['UploadError'] = None 
                murakami_output['RTTValue'] = summary["RTT"]['Value']
                murakami_output['RTTUnit'] = summary["RTT"]['Unit']
            else:
                logger.warn("ndt7 test failed: %s", output.stderr.splitlines())
            return json.dumps(murakami_output)
        else:
            raise RunnerError(
                "ndt7-client",
                "Executable ndt7-client does not exist, please install ndt7-client-go.",
            )