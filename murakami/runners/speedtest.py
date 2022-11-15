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
            title="Ookla-Speedtest",
            description="The Ookla/Speedtest.net CLI client  (https://www.speedtest.net/apps/cli).",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )
     
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

            return json.dumps(murakami_output)

        else:
            raise RunnerError(
                "speedtest",
                "Executable does not exist, please install speedtest.")
