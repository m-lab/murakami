import logging
import shutil
import subprocess
import json
import datetime

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class OONIProbeClient(MurakamiRunner):
    """Run ooniprobe's unattended tests (websites, instant messaging, etc.)."""
    def __init__(self, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            title="ooniprobe",
            description="Test the blocking of websites and apps.",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id
        )

    def _start_test(self):
        logger.info("Starting ooniprobe test...")
        if shutil.which("ooniprobe") is not None:
            output = None
            
            # Empty the ooniprobe database.
            logger.info("Emptying ooniprobe database...")
            cmdargs = [
                "ooniprobe",
                "reset",
                "--force",
            ]
            try:
                output = subprocess.run(
                    cmdargs,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                raise RunnerError(
                    "ooniprobe reset --force returned a non-zero exit code."
                )

            # Tell ooniprobe to skip the onboarding process.
            logger.info("Skipping onboarding process...")
            cmdargs = [
                "ooniprobe",
                "onboard",
                "--yes",
            ]

            try:
                output = subprocess.run(
                    cmdargs,
                    check=True,
                    stderr=subprocess.PIPE
                )
            except subprocess.CalledProcessError as e:
                raise RunnerError(
                    "ooniprobe onboard --yes returned a non-zero exit code. (err: " + output.stderr + ")"
                )
            
            # Run "ooniprobe run unattended" to start the tests.
            logger.info("Running ooniprobe tests...")
            starttime = datetime.datetime.utcnow()
            cmdargs = [
                "ooniprobe",
                "--software-name=murakami-ooniprobe",
                "run",
                "unattended"
            ]

            try:
                output = subprocess.run(
                    cmdargs,
                    check=True,
                    stderr=subprocess.PIPE
                )
            except subprocess.CalledProcessError as e:
                raise RunnerError(
                    "ooniprobe run unattended returned a non-zero exit code. (err: " + output.stderr + ")"
                )
            endtime = datetime.datetime.utcnow()
           
            # If the previous commands succeeded, then we can parse the output
            # of "ooniprobe list --batch", which only contains the results of
            # the current run (since the database was emptied beforehand).
            logging.info("Reading ooniprobe results...")
            cmdargs = [
                "ooniprobe",
                "list",
                "--batch"
            ]

            try:
                output = subprocess.run(
                    cmdargs,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except subprocess.CalledProcessError as e:
                raise RunnerError(
                    "ooniprobe list --batch returned a non-zero exit code. (err: " + output.stderr + ")"
                )
            
            # Parse the output of "ooniprobe list --batch". The output is in
            # JSONL format, and we need to only parse lines containing an
            # "id" field.
            results = []
            try:
                results = [json.loads(line) for line in output.stdout.splitlines()]
            except json.decoder.JSONDecodeError as e:
                raise RunnerError(
                    "ooniprobe list --batch returned invalid JSON. (err: " + str(e) + ")"
                )

            test_results = {}
            for js in results:
                # If the JSON contains an "id" field, then it is a test result.
                # Get the corresponding nettest summary data with:
                # "ooniprobe list <id> --batch".
                if "id" in js["fields"]:
                    # Get the test's name.
                    test_name = js["fields"]["name"]

                    cmdargs = [
                        "ooniprobe",
                        "list",
                        str(js["fields"]["id"]),
                        "--batch"
                    ]

                    try:
                        output = subprocess.run(
                            cmdargs,
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    except subprocess.CalledProcessError as e:
                        raise RunnerError(
                            "ooni probe list <id> --batch returned a non-zero exit code. (err: " + output.stderr + ")"
                        )

                    try:
                        test_measurements = [json.loads(line) for line in output.stdout.splitlines()]
                        test_results[test_name] = test_measurements
                    except json.decoder.JSONDecodeError as e:
                        raise RunnerError(
                            "ooni probe list <id> --batch returned invalid JSON. (err: " + str(e) + ")"
                        )

            # Wrap the test results in a JSON that's compatible with Murakami.
            murakami_output = {
                'TestName': "ooniprobe",
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'MurakamiLocation': self._location,
                'MurakamiConnectionType': self._connection_type,
                'MurakamiNetworkType': self._network_type,
                'MurakamiDeviceID': self._device_id,
            }

            murakami_output['TestResults'] = test_results
           
            return json.dumps(murakami_output)