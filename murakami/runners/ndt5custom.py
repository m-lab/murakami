import logging
import shutil
import subprocess
import uuid
import datetime
import json
import pkg_resources

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt5ClientCustom(MurakamiRunner):
    """Run NDT5 test."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="ndt5custom",
            description="The Network Diagnostic Tool v5 test.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )

        self._server_selection = {}

        # Load all the available server selection algorithms.
        for entry_point in pkg_resources.iter_entry_points(
            "murakami.selection"
        ):
            self._server_selection[entry_point.name] = entry_point.load()()

    def _run_client(self, args):
        starttime = datetime.datetime.utcnow()
        output = subprocess.run(
            args,
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

    def _start_test(self):
        logger.info("Starting ndt5custom test...")
        
        # Check that a configuration file has been specified
        if "config" not in self._config:
            raise RunnerError(
                'ndt5custom',
                'No configuration file specified for the custom runner, \
                    skipping.')
        
        # Check that the ndt5-client executable is available.
        if shutil.which('ndt5-client') is None:
            raise RunnerError(
                'ndt5custom',
                "Executable ndt5-client does not exist, please install ndt5-client-go.",
            )

        custom_config = {}
        try:
            with open(self._config['config']) as config_file:
                custom_config = json.load(config_file)
        except IOError as err:
            raise RunnerError(
            'ndt5custom',
            'Cannot open the custom configuration file: ' + str(err))
        
        # Get all the servers to run measurements against from the config,
        # applying the corresponding selection algorithm.
        servers = set()
        for group in custom_config.get('serverGroups', []):
            # the default selection algorithm is 'random'
            selection = group.get('selection', 'random')
            if selection not in self._server_selection:
                raise RunnerError(
                'ndt5custom',
                'Invalid server selection algorithm specified:' +
                selection)

            servers = servers | self._server_selection[selection].get_servers(
                group.get('servers', []))

        # Run a measurement against each of the selected servers.
        results = []
        for server in servers:
            cmdargs = [
                "ndt5-client",
                "-protocol=ndt5",
                "-format=json",
                "-quiet",
                "-server=" + server
            ]
            logger.info("Running ndt5custom measurement (server): " + server)
            results.append(self._run_client(cmdargs))

        return results
