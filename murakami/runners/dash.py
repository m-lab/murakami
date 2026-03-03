"""
This module contains the DASH test runner.
"""
import datetime
import json
import logging
import shutil
import subprocess

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

    def _start_test(self):
        logger.info("Starting DASH test...")
        if shutil.which("dash-client") is None:
            raise RunnerError(
                "dash",
                "Executable dash-client does not exist, please install DASH.")

        starttime = datetime.datetime.now(datetime.timezone.utc)
        output = subprocess.run(
            ["dash-client", "-format=json"],
            check=False,
            text=True,
            capture_output=True,
        )
        endtime = datetime.datetime.now(datetime.timezone.utc)

        murakami_output = {
            'TestName': "dash",
            'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'MurakamiLocation': self._location,
            'MurakamiConnectionType': self._connection_type,
            'MurakamiNetworkType': self._network_type,
            'MurakamiDeviceID': self._device_id,
        }

        if output.returncode != 0:
            logger.warning("DASH test completed with errors.")
            murakami_output['TestError'] = output.stderr or output.stdout
            murakami_output['ServerURL'] = None
            murakami_output['Latency'] = None
            murakami_output['LatencyUnit'] = None
            murakami_output['DownloadSpeed'] = None
            murakami_output['DownloadSpeedUnit'] = None
            murakami_output['SegmentDownloadTimes'] = None
            murakami_output['SegmentRates'] = None
            return json.dumps(murakami_output)

        # Parse each JSON line from dash-client output
        segments = []
        server_url = None
        for line in output.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                # Each line is a segment result
                segments.append(entry)
                if server_url is None:
                    server_url = entry.get('ServerURL')
            except json.JSONDecodeError:
                logger.warning("Could not parse DASH output line: %s", line)
                continue

        logger.info("DASH test complete. Parsed %d segments.", len(segments))

        if segments:
            # Compute summary metrics across all segments
            rates = [s.get('Rate', 0) for s in segments if 'Rate' in s]
            elapsed_times = [s.get('Elapsed', 0) for s in segments if 'Elapsed' in s]
            received = [s.get('Received', 0) for s in segments if 'Received' in s]

            avg_speed = sum(rates) / len(rates) if rates else None
            total_received = sum(received) if received else None

            murakami_output['ServerURL'] = server_url
            murakami_output['DownloadSpeed'] = avg_speed
            murakami_output['DownloadSpeedUnit'] = 'kbit/s'
            murakami_output['TotalBytesReceived'] = total_received
            murakami_output['TotalBytesReceivedUnit'] = 'bytes'
            murakami_output['Latency'] = segments[0].get('Connect', None)
            murakami_output['LatencyUnit'] = 's'
            murakami_output['NumSegments'] = len(segments)
            murakami_output['SegmentRates'] = rates
            murakami_output['SegmentDownloadTimes'] = elapsed_times
        else:
            logger.warning("No segments parsed from DASH output.")
            murakami_output['TestError'] = "No segments parsed from output."
            murakami_output['ServerURL'] = None
            murakami_output['DownloadSpeed'] = None
            murakami_output['DownloadSpeedUnit'] = None
            murakami_output['Latency'] = None
            murakami_output['LatencyUnit'] = None
            murakami_output['SegmentRates'] = None
            murakami_output['SegmentDownloadTimes'] = None

        return json.dumps(murakami_output)
