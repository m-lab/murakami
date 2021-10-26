import logging
import shutil
import subprocess
import uuid
import datetime
import json

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class SpeedtestClient(MurakamiRunner):
    """Run Speedtest.net tests."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="Speedtest-cli-multi-stream",
            description="The Speedtest.net multi-stream test (https://github.com/sivel/speedtest-cli).",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )

    @staticmethod
    def _parse_summary(output):
        """Parses the speedtest-cli summary.

        Args:
            output: stdout of the process

        Returns:
            A dict containing a summary of the test.

        Raises:
            JSONDecodeError: if the output cannot be parsed as JSON.
        """
        murakami_output = {}

        if output.returncode == 0:
            summary = {}
            summary = json.loads(output.stdout)

            murakami_output['DownloadValue'] = summary.get('download')
            murakami_output['DownloadUnit'] = 'Bit/s'
            murakami_output['UploadValue'] = summary.get('upload')
            murakami_output['UploadUnit'] = 'Bit/s'
            murakami_output['Ping'] = summary.get('ping')
            murakami_output['PingUnit'] = 'ms'
            murakami_output['BytesSent'] = summary.get('bytes_sent')
            murakami_output['BytesReceived'] = summary.get('bytes_received')
            murakami_output['Share'] = summary.get('share')
            murakami_output['Timestamp'] = summary.get('timestamp')

            server = summary.get('server')
            client = summary.get('client')

            if server is not None:
                murakami_output['ServerURL'] = server.get('url')
                murakami_output['ServerLat'] = server.get('lat')
                murakami_output['ServerLon'] = server.get('lon')
                murakami_output['ServerName'] = server.get('name')
                murakami_output['ServerCountry'] = server.get('country')
                murakami_output['ServerCountryCode'] = server.get('cc')
                murakami_output['ServerSponsor'] = server.get('sponsor')
                murakami_output['ServerID'] = server.get('id')
                murakami_output['ServerHost'] = server.get('host')
                murakami_output['ServerDistance'] = server.get('d')
                murakami_output['ServerLatency'] = server.get('latency')
                murakami_output['ServerLatencyUnit'] = 'ms'

            if client is not None:
                murakami_output['ClientIP'] = client.get('ip')
                murakami_output['ClientLat'] = client.get('lat')
                murakami_output['ClientLon'] = client.get('lon')
                murakami_output['Isp'] = client.get('isp')
                murakami_output['IspRating'] = client.get('isprating')
                murakami_output['Rating'] = client.get('rating')
                murakami_output['IspDownloadAvg'] = client.get('ispdlavg')
                murakami_output['IspUploadAvg'] = client.get('ispulavg')
                murakami_output['LoggedIn'] = client.get('loggedin')
                murakami_output['Country'] = client.get('country')

            return murakami_output
        else:
            # Set TestError and every other field to None.
            murakami_output['TestError'] = output.stderr

            murakami_output['DownloadValue'] = None
            murakami_output['DownloadUnit'] = None
            murakami_output['UploadValue'] = None
            murakami_output['UploadUnit'] = None
            murakami_output['BytesSent'] = None
            murakami_output['BytesReceived'] = None
            murakami_output['Share'] = None
            murakami_output['Timestamp'] = None
            murakami_output['ServerURL'] = None
            murakami_output['ServerLat'] = None
            murakami_output['ServerLon'] = None
            murakami_output['ServerName'] = None
            murakami_output['ServerCountry'] = None
            murakami_output['ServerCountryCode'] = None
            murakami_output['ServerSponsor'] = None
            murakami_output['ServerID'] = None
            murakami_output['ServerHost'] = None
            murakami_output['ServerDistance'] = None
            murakami_output['ServerLatency'] = None
            murakami_output['ServerLatencyUnit'] = None
            murakami_output['ClientIP'] = None
            murakami_output['ClientLat'] = None
            murakami_output['ClientLon'] = None
            murakami_output['Isp'] = None
            murakami_output['IspRating'] = None
            murakami_output['Rating'] = None
            murakami_output['IspDownloadAvg'] = None
            murakami_output['IspUploadAvg'] = None
            murakami_output['LoggedIn'] = None
            murakami_output['Country'] = None

        return murakami_output
        
    def _start_test(self):
        logger.info("Starting Speedtest multi-stream test...")
        if shutil.which("speedtest-cli") is not None:

            starttime = datetime.datetime.utcnow()
            output = subprocess.run(["speedtest-cli", "--json"],
                                    text=True,
                                    capture_output=True)
            endtime = datetime.datetime.utcnow()

            murakami_output = {
                'TestName': "speedtest-cli-multi-stream",
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'MurakamiLocation': self._location,
                'MurakamiConnectionType': self._connection_type,
                'MurakamiNetworkType': self._network_type,
                'MurakamiDeviceID': self._device_id,
            }

            murakami_output.update(self._parse_summary(output))
            return json.dumps(murakami_output)

        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest-cli.")
