import logging
import shutil
import subprocess
import uuid

from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)


class RunDash(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        print("perform dash action")
        self.thing.start_test()


class DashClient(MurakamiRunner):
    """Run Dash tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(name="dash", config=config, data_cb=data_cb)

        self._thing = Thing(
            "urn:dev:ops:dash-client",
            "Dash Client",
            ["OnOffSwitch", "Client"],
            "A client running Dash tests",
        )

        self._thing.add_property(
            Property(
                self,
                "on",
                Value(True, lambda v: print("On-State is now", v)),
                metadata={
                    "@type": "OnOffProperty",
                    "title": "On/Off",
                    "type": "boolean",
                    "description": "Whether the client is running",
                },
            ))

        self._thing.add_available_action(
            "run",
            {
                "title": "Run",
                "description": "Run tests",
                "input": {
                    "type": "object",
                    "required": ["download", "upload"],
                    "properties": {
                        "download": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                        "upload": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                    },
                },
            },
            RunDash,
        )

        self._thing.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def _start_test(self):
        if shutil.which("dash-client") is not None:
            output = subprocess.run([
                "rm -f ./certs/*.pem &&                      \
                ./mkcerts.bash &&                            \
                sudo chown root:root ./certs/*.pem &&        \
                docker run --network=bridge                  \
                           --publish=80:8888                 \
                           --publish=443:4444                \
                           --publish=9990:9999               \
                           --volume `pwd`/certs:/certs:ro    \
                           --volume `pwd`/datadir:/datadir   \
                           --read-only                       \
                           --cap-drop=all                    \
                           neubot/dash                       \
                           -datadir /datadir                 \
                           -http-listen-address :8888        \
                           -https-listen-address :4444       \
                           -prometheusx.listen-address :9999 \
                           -tls-cert /certs/cert.pem         \
                           -tls-key /certs/key.pem"
                           ],
                            check=True,
                            text=True,
                            capture_output=True)
        else:
            raise RunnerError(
                "dash",
                "Executable dash-client does not exist, please install DASH.")
        return output.stdout
