import logging
import shutil
import subprocess
import uuid
import datetime
import json

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt5Client(MurakamiRunner):
    """Run NDT5 test."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="ndt5",
            description="The Network Diagnostic Tool v5 test.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )

    def _start_test(self):
        logger.info("Starting NDT5 test...")
        if shutil.which("ndt5-client") is not None:
            cmdargs = [
                "ndt5-client",
                "-protocol=ndt5",
                "-format=json",
                "-quiet"
            ]

            if "host" in self._config:
                logger.info("host value set:"+self._config['host'])
                cmdargs.append('-server='+self._config['host'])

            starttime = datetime.datetime.utcnow()
            output = subprocess.run(
                cmdargs,
                text=True,
                capture_output=True,
            )
            endtime = datetime.datetime.utcnow()

            murakami_output = {
                'TestName': "ndt5",
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'MurakamiLocation': self._location,
                'MurakamiConnectionType': self._connection_type,
                'MurakamiNetworkType': self._network_type,
                'MurakamiDeviceID': self._device_id,
            }

            if output.returncode == 0:
                # Parse ndt5 summary.
                summary = {}
                try:
                    summary = json.loads(output.stdout)
                except json.JSONDecodeError:
                    raise RunnerError(
                        'ndt5-client',
                        'ndt5-client did not return a valid JSON summary.')

                logger.info("ndt5 test completed successfully.")

                # Parse ndt7-client-go's summary JSON and generate Murakami's
                # output format.
                download = summary.get('Download')
                upload = summary.get('Upload')
                retrans = summary.get('DownloadRetrans')
                min_rtt = summary.get('MinRTT')

                murakami_output['ServerName'] = summary.get('ServerFQDN')
                murakami_output['ServerIP'] = summary.get('ServerIP')
                murakami_output['ClientIP'] = summary.get('ClientIP')
                murakami_output['DownloadUUID'] = summary.get('DownloadUUID')
                if download is not None:
                    murakami_output['DownloadValue'] = download.get('Value')
                    murakami_output['DownloadUnit'] = download.get('Unit')
                if upload is not None:
                    murakami_output['UploadValue'] = upload.get('Value')
                    murakami_output['UploadUnit'] = upload.get('Unit')
                if retrans is not None:
                    murakami_output['DownloadRetransValue'] = retrans.get('Value')
                    murakami_output['DownloadRetransUnit'] = retrans.get('Unit')
                if min_rtt is not None:
                    murakami_output['MinRTTValue'] = min_rtt.get('Value')
                    murakami_output['MinRTTUnit'] = min_rtt.get('Unit')
            else:
                logger.warn("ndt5 test completed with errors.")

                # Consider any output as 'TestError'.
                murakami_output['TestError'] = output.stdout

                # All the other fields are set to None (which will become null
                # in the JSON.)
                murakami_output['ServerName'] = None
                murakami_output['ServerIP'] = None
                murakami_output['ClientIP'] = None
                murakami_output['DownloadUUID'] = None
                murakami_output['DownloadValue'] = None
                murakami_output['DownloadUnit'] = None
                murakami_output['UploadValue'] = None
                murakami_output['UploadUnit'] = None
                murakami_output['DownloadRetransValue'] = None
                murakami_output['DownloadRetransUnit'] = None
                murakami_output['MinRTTValue'] = None
                murakami_output['MinRTTUnit'] = None
            return json.dumps(murakami_output)
        else:
            raise RunnerError(
                "ndt5-client",
                "Executable ndt5-client does not exist, please install ndt5-client-go.",
            )
