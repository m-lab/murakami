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
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="ndt7",
            description="The Network Diagnostic Tool v7 test.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )

    def _start_test(self):
        logger.info("Starting ndt7 test...")
        if shutil.which("ndt7-client") is not None:
            cmdargs = [
                "ndt7-client",
                "-format=json",
                "-quiet",
                "-scheme=ws"
            ]

            if "host" in self._config:
                cmdargs.append("-server=" + self._config['host'])
                insecure = self._config.get('insecure', True)
                if insecure:
                    cmdargs.append('-no-verify')

            starttime = datetime.datetime.utcnow()
            output = subprocess.run(
                cmdargs,
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
                'MurakamiNetworkType': self._network_type,
                'MurakamiDeviceID': self._device_id,
            }

            if output.returncode == 0:
                # Parse ndt7 summary.
                summary = {}
                try:
                    summary = json.loads(output.stdout)
                except json.JSONDecodeError:
                    raise RunnerError(
                        'ndt7-client',
                        'ndt7-client did not return a valid JSON summary.'
                    )
                logger.info("ndt7 test completed successfully.")

                # Parse ndt7-client-go's summary JSON and generate Murakami's
                # output format.
                download = summary.get('Download')
                upload = summary.get('Upload')
                retrans = summary.get('DownloadRetrans')
                minrtt = summary.get('MinRTT')

                murakami_output['ServerName'] = summary.get('ServerFQDN')
                murakami_output['ServerIP'] = summary.get('ServerIP')
                murakami_output['ClientIP'] = summary.get('ClientIP')
                murakami_output['DownloadUUID'] = summary.get('DownloadUUID')
                if download is not None:
                    murakami_output['DownloadValue'] = download.get('Value')
                    murakami_output['DownloadUnit'] = download.get('Unit')
                    murakami_output['DownloadError'] = None
                if upload is not None:
                    murakami_output['UploadValue'] = upload.get('Value')
                    murakami_output['UploadUnit'] = upload.get('Unit')
                    murakami_output['UploadError'] = None
                if retrans is not None:
                    murakami_output['DownloadRetransValue'] = retrans.get('Value')
                    murakami_output['DownloadRetransUnit'] = retrans.get('Unit')
                if minrtt is not None:
                    murakami_output['MinRTTValue'] = minrtt.get('Value')
                    murakami_output['MinRTTUnit'] = minrtt.get('Unit')
            else:
                logger.warn("ndt7 test completed with errors.")

                # Parse error line(s) and generate summary with UploadError and
                # DownloadError only, if available.
                errors = output.stdout.splitlines()
                for j in errors:
                    try:
                        message = json.loads(j)
                        if message['Value']['Test'] == 'upload':
                            murakami_output['UploadError'] = (
                                message['Value']['Failure']
                            )
                        elif message['Value']['Test'] == 'download':
                            murakami_output['DownloadError']= (
                                message['Value']['Failure']
                            )
                    except Exception as exc:
                        logger.error("Cannot parse error message: %s", exc)

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
                murakami_output['RTTValue'] = None
                murakami_output['RTTUnit'] = None
            return json.dumps(murakami_output)
        else:
            raise RunnerError(
                "ndt7-client",
                "Executable ndt7-client does not exist, please install ndt7-client-go.",
            )
