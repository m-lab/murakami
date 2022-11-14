import logging
import shutil
import subprocess
import uuid
import datetime
import json
import codecs

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

        summary = {}
        summary = json.loads(output)

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
        
    def _start_test(self):
        logger.info("Starting Ookla Speedtest...")
        if shutil.which("speedtest") is not None:

            starttime = datetime.datetime.utcnow()
            output = subprocess.check_output(["speedtest", "--format=json"],stdin=None, stderr=subprocess.PIPE, shell=False, universal_newlines=False)
            
            endtime = datetime.datetime.utcnow()

            murakami_output = {}
            murakami_output['TestName'] = "ookla-speedtest"
            murakami_output['TestStartTime'] = starttime.strftime('%Y-%m-%dT%H:%M:%S.%f')
            murakami_output['TestEndTime'] = endtime.strftime('%Y-%m-%dT%H:%M:%S.%f')
            murakami_output['MurakamiLocation'] = self._location
            murakami_output['MurakamiConnectionType'] = self._connection_type
            murakami_output['MurakamiNetworkType'] = self._network_type
            murakami_output['MurakamiDeviceID'] = self._device_id

            output_json = output.decode('utf8')
    
            summary = {}
            summary = json.loads(output_json)

            ping = summary.get('ping')
            download = summary.get('download')
            download_latency = download.get('latency')
            upload = summary.get('upload')
            upload_latency = upload.get('latency')
            interface = summary.get('interface')
            server = summary.get('server')
            result = summary.get('result')

            murakami_output['Type'] = summary.get('type')
            murakami_output['Timestamp'] = summary.get('timestamp')
            murakami_output['PingJitter'] = ping.get('jitter')
            murakami_output['PingLatency'] = ping.get('latency')
            murakami_output['PingLow'] = ping.get('low')
            murakami_output['PingHigh'] = ping.get('high')
            murakami_output['DownloadBandwidth'] = download.get('bandwidth')
            murakami_output['DownloadUnit'] = 'Bit/s'
            murakami_output['DownloadBytes'] = download.get('bytes')
            murakami_output['DownloadElapsed'] = download.get('elapsed')
            murakami_output['DownloadLatencyIqm'] = download_latency.get('iqm')
            murakami_output['DownloadLatencyLow'] = download_latency.get('low')
            murakami_output['DownloadLatencyHigh'] = download_latency.get('high')
            murakami_output['DownloadLatencyJitter'] = download_latency.get('jitter')
            murakami_output['UploadBandwidth'] = upload.get('bandwidth')
            murakami_output['UploadUnit'] = 'Bit/s'
            murakami_output['UploadBytes'] = upload.get('bytes')
            murakami_output['UploadElapsed'] = upload.get('elapsed')
            murakami_output['UploadLatencyIqm'] = upload_latency.get('iqm')
            murakami_output['UploadLatencyLow'] = upload_latency.get('low')
            murakami_output['UploadLatencyHigh'] = upload_latency.get('high')
            murakami_output['UploadLatencyJitter'] = upload_latency.get('jitter')
            murakami_output['PacketLoss'] = summary.get('packetLoss')
            murakami_output['Isp'] = summary.get('isp')
            murakami_output['InterfaceInternalIp'] = interface.get('internalIp')
            murakami_output['InterfaceName'] = interface.get('name')
            murakami_output['InterfaceMacAddr'] = interface.get('macAddr')
            murakami_output['InterfaceIsVpn'] = interface.get('isVpn')
            murakami_output['InterfaceExternalIp'] = interface.get('externalIp')
            murakami_output['ServerId'] = server.get('id')
            murakami_output['ServerHost'] = server.get('host')
            murakami_output['ServerPort'] = server.get('port')
            murakami_output['ServerName'] = server.get('name')
            murakami_output['ServerLocation'] = server.get('location')
            murakami_output['ServerCountry'] = server.get('country')
            murakami_output['ServerIp'] = server.get('ip')
            murakami_output['ResultId'] = result.get('id')
            murakami_output['ResultUrl'] = result.get('url')
            murakami_output['ResultPersisted'] = result.get('persisted')

#            murakami_output.update(self._parse_summary(output_json))

            return json.dumps(murakami_output)

        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest.")
