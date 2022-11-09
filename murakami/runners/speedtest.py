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
            title="Ookla Speedtest",
            description="The Ookla/Speedtest.net CLI client  (https://www.speedtest.net/apps/cli).",
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

            murakami_output['Type'] = summary.get('type')
            murakami_output['Timestamp'] = summary.get('timestamp')
            murakami_output['PingJitter'] = summary.get['ping']['jitter']
            murakami_output['PingLatency'] = summary.get['ping']['latency']
            murakami_output['PingLow'] = summary.get['ping']['low']
            murakami_output['PingHigh'] = summary.get['ping']['high']
            murakami_output['DownloadBandwidth'] = summary.get['download']['bandwidth']
            murakami_output['DownloadUnit'] = 'Bit/s'
            murakami_output['DownloadBytes'] = summary.get['download']['bytes']
            murakami_output['DownloadElapsed'] = summary.get['download']['elapsed']
            murakami_output['DownloadLatencyIqm'] = summary.get['download']['latency']['iqm']
            murakami_output['DownloadLatencyLow'] = summary.get['download']['latency']['low']
            murakami_output['DownloadLatencyHigh'] = summary.get['download']['latency']['high']
            murakami_output['DownloadLatencyJitter'] = summary.get['download']['latency']['jitter']
            murakami_output['UploadBandwidth'] = summary.get['upload']['bandwidth']
            murakami_output['UploadUnit'] = 'Bit/s'
            murakami_output['UploadBytes'] = summary.get['upload']['bytes']
            murakami_output['UploadElapsed'] = summary.get['upload']['elapsed']
            murakami_output['UploadLatencyIqm'] = summary.get['upload']['latency']['iqm']
            murakami_output['UploadLatencyLow'] = summary.get['upload']['latency']['low']
            murakami_output['UploadLatencyHigh'] = summary.get['upload']['latency']['high']
            murakami_output['UploadLatencyJitter'] = summary.get['upload']['latency']['jitter']
            murakami_output['PacketLoss'] = summary.get('packetLoss')
            murakami_output['Isp'] = summary.get('isp')
            murakami_output['InterfaceInternalIp'] = summary.get['interface']['internalIp']
            murakami_output['InterfaceName'] = summary.get['interface']['name']
            murakami_output['InterfaceMacAddr'] = summary.get['interface']['macAddr']
            murakami_output['InterfaceIsVpn'] = summary.get['interface']['isVpn']
            murakami_output['InterfaceExternalIp'] = summary.get['interface']['externalIp']
            murakami_output['ServerId'] = summary.get['server']['id']
            murakami_output['ServerHost'] = summary.get['server']['host']
            murakami_output['ServerPort'] = summary.get['server']['port']
            murakami_output['ServerName'] = summary.get['server']['name']
            murakami_output['ServerLocation'] = summary.get['server']['location']
            murakami_output['ServerCountry'] = summary.get['server']['country']
            murakami_output['ServerIp'] = summary.get['server']['ip']
            murakami_output['ResultId'] = summary.get['result']['id']
            murakami_output['ResultUrl'] = summary.get['result']['url']
            murakami_output['ResultPersisted'] = summary.get['result']['persisted']

            return murakami_output
        else:
            # Set TestError and every other field to None.
            murakami_output['TestError'] = output.stderr

            murakami_output['Type'] = None
            murakami_output['Timestamp'] = None
            murakami_output['PingJitter'] = None
            murakami_output['PingLatency'] = None
            murakami_output['PingLow'] = None
            murakami_output['PingHigh'] = None
            murakami_output['DownloadBandwidth'] = None
            murakami_output['DownloadUnit'] = None
            murakami_output['DownloadBytes'] = None
            murakami_output['DownloadElapsed'] = None
            murakami_output['DownloadLatencyIqm'] = None
            murakami_output['DownloadLatencyLow'] = None
            murakami_output['DownloadLatencyHigh'] = None
            murakami_output['DownloadLatencyJitter'] = None
            murakami_output['UploadBandwidth'] = None
            murakami_output['UploadUnit'] = None
            murakami_output['UploadBytes'] = None
            murakami_output['UploadElapsed'] = None
            murakami_output['UploadLatencyIqm'] = None
            murakami_output['UploadLatencyLow'] = None
            murakami_output['UploadLatencyHigh'] = None
            murakami_output['UploadLatencyJitter'] = None
            murakami_output['PacketLoss'] = None
            murakami_output['Isp'] = None
            murakami_output['InterfaceInternalIp'] = None
            murakami_output['InterfaceName'] = None
            murakami_output['InterfaceMacAddr'] = None
            murakami_output['InterfaceIsVpn'] = None
            murakami_output['InterfaceExternalIp'] = None
            murakami_output['ServerId'] = None
            murakami_output['ServerHost'] = None
            murakami_output['ServerPort'] = None
            murakami_output['ServerName'] = None
            murakami_output['ServerLocation'] = None
            murakami_output['ServerCountry'] = None
            murakami_output['ServerIp'] = None
            murakami_output['ResultId'] = None
            murakami_output['ResultUrl'] = None
            murakami_output['ResultPersisted'] = None

        return murakami_output
        
    def _start_test(self):
        logger.info("Starting Ookla Speedtest...")
        if shutil.which("speedtest") is not None:

            starttime = datetime.datetime.utcnow()
            output = subprocess.run(["speedtest", "--format=json"])
            endtime = datetime.datetime.utcnow()

            murakami_output = {}
            murakami_output['TestName'] = "ookla-speedtest"
            murakami_output['TestStartTime'] = starttime.strftime('%Y-%m-%dT%H:%M:%S.%f')
            murakami_output['TestEndTime'] = endtime.strftime('%Y-%m-%dT%H:%M:%S.%f')
            murakami_output['MurakamiLocation'] = self._location
            murakami_output['MurakamiConnectionType'] = self._connection_type
            murakami_output['MurakamiNetworkType'] = self._network_type
            murakami_output['MurakamiDeviceID'] = self._device_id

            murakami_output.update(self._parse_summary(output))

            return json.dumps(murakami_output)

        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest.")
