import logging
import shutil
import subprocess
import uuid
import json
import datetime
import pkg_resources

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class Ndt7ClientCustom(MurakamiRunner):
    """Run ndt7 test."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="ndt7custom",
            description="The Network Diagnostic Tool v7 test.",
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

    def _start_test(self):
        logger.info("Starting ndt7 test...")

        # Check that a configuration file has been specified
        if "config" not in self._config:
            raise RunnerError(
                'ndt7custom',
                'No configuration file specified for the custom runner, \
                    skipping.')
        
        # Check that the ndt7-client executable is available.
        if shutil.which('ndt7-client') is None:
            raise RunnerError(
                'ndt7custom',
                "Executable ndt7-client does not exist, please install ndt7-client-go.",
            )

        custom_config = {}
        try:
            with open(self._config['config']) as config_file:
                custom_config = json.load(config_file)
        except IOError as err:
            raise RunnerError(
            'ndt7custom',
            'Cannot open the custom configuration file: ' + str(err))
        
        # Get all the servers to run measurements against from the config,
        # applying the corresponding selection algorithm.
        servers = set()
        for group in custom_config.get('serverGroups', []):
            # the default selection algorithm is 'random'
            selection = group.get('selection', 'random')
            if selection not in self._server_selection:
                raise RunnerError(
                'ndt7custom',
                'Invalid server selection algorithm specified:' +
                selection)

            servers = servers | self._server_selection[selection].get_servers(
                group.get('servers', []))

        # Run a measurement against each of the selected servers.
        results = []
        for server in servers:
            cmdargs = [
                "ndt7-client",
                "-format=json",
                "-quiet",
                "-scheme=ws",
                "-server=" + server
            ]
            
            insecure = self._config.get('insecure', True)
            if insecure:
                cmdargs.append('-no-verify')
            
            logger.info("Running ndt7custom measurement (server): " + server)
            results.append(self._run_client(cmdargs))
        
        # Check for additional countries/regions specified and run the client
        # using the locate service for each of them.
        countries = custom_config.get('countries', [])
        for country in countries:
            cmdargs = [
                "ndt7-client",
                "-format=json",
                "-quiet",
                "-scheme=ws",
                "-locate.url=https://locate.measurementlab.net/v2/nearest/?country=" + country
            ]
            logger.info("Running ndt7custom measurement (country): " + country)
            results.append(self._run_client(cmdargs))
        
        regions = custom_config.get('regions', [])
        for region in regions:
            cmdargs = [
                "ndt7-client",
                "-format=json",
                "-quiet",
                "-scheme=ws",
                "-locate.url=https://locate.measurementlab.net/v2/nearest/?region=" + region
            ]
            logger.info("Running ndt7custom measurement (region): " + region)
            results.append(self._run_client(cmdargs))

        return results
        
