import logging
import shutil
import subprocess
import uuid

from webthing import Action, Event, Property, Thing, Value

from murakami.errors import RunnerError
from murakami.runner import MurakamiRunner

logger = logging.getLogger(__name__)

NDT5_SCHEMA = [
    "CurMSS",
    "X_Rcvbuf",
    "X_Sndbuf",
    "AckPktsIn",
    "AckPktsOut",
    "BytesRetrans",
    "CongAvoid",
    "CongestionOverCount",
    "CongestionSignals",
    "CountRTT",
    "CurCwnd",
    "CurRTO",
    "CurRwinRcvd",
    "CurRwinSent",
    "CurSsthresh",
    "DSACKDups",
    "DataBytesIn",
    "DataBytesOut",
    "DataPktsIn",
    "DataPktsOut",
    "DupAcksIn",
    "ECNEnabled",
    "FastRetran",
    "MaxCwnd",
    "MaxMSS",
    "MaxRTO",
    "MaxRTT",
    "MaxRwinRcvd",
    "MaxRwinSent",
    "MaxSsthresh",
    "MinMSS",
    "MinRTO",
    "MinRTT",
    "MinRwinRcvd",
    "MinRwinSent",
    "NagleEnabled",
    "OtherReductions",
    "PktsIn",
    "PktsOut",
    "PktsRetrans",
    "RcvWinScale",
    "SACKEnabled",
    "SACKsRcvd",
    "SendStall",
    "SlowStart",
    "SampleRTT",
    "SmoothedRTT",
    "SndWinScale",
    "SndLimTimeRwin",
    "SndLimTimeCwnd",
    "SndLimTimeSender",
    "SndLimTransRwin",
    "SndLimTransCwnd",
    "SndLimTransSender",
    "SndLimBytesRwin",
    "SndLimBytesCwnd",
    "SndLimBytesSender",
    "SubsequentTimeouts",
    "SumRTT",
    "Timeouts",
    "TimestampsEnabled",
    "WinScaleRcvd",
    "WinScaleSent",
    "DupAcksOut",
    "StartTimeUsec",
    "Duration",
    "c2sData",
    "c2sAck",
    "s2cData",
    "s2cAck",
    "half_duplex",
    "link",
    "congestion",
    "bad_cable",
    "mismatch",
    "spd",
    "bw",
    "loss",
    "avgrtt",
    "waitsec",
    "timesec",
    "order",
    "rwintime",
    "sendtime",
    "cwndtime",
    "rwin",
    "swin",
    "cwin",
    "rttsec",
    "Sndbuf",
    "aspd",
    "CWND-Limited",
    "minCWNDpeak",
    "maxCWNDpeak",
    "CWNDpeaks",
]


class RunLibndt(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        logger.info("Performing ndt5 test")
        self.thing.start_test()


class LibndtClient(MurakamiRunner):
    """Run LibNDT tests."""
    def __init__(self, config=None, data_cb=None):
        super().__init__(name="ndt5", config=config, data_cb=data_cb)

        self.thing = Thing(
            "urn:dev:ops:libndt-client",
            "LibNDT Client",
            ["OnOffSwitch", "Client"],
            "A client running LibNDT tests",
        )

        self.thing.add_property(
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

        self.thing.add_available_action(
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
            RunLibndt,
        )

        self.thing.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def _start_test(self):
        logger.info("Starting NDT test...")
        if shutil.which("libndt-client") is not None:
            output = subprocess.run(
                [
                    "libndt-client",
                    "--download",
                    "--upload",
                    "--lookup-policy=closest",
                    "--json",
                    "--websocket",
                    "--tls",
                    "--batch",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            json = dict(
                zip(
                    NDT5_SCHEMA,
                    [
                        str(n) if not n.replace(".", "", 1).isdigit() else
                        float(n) if "." in n else int(n)
                        for n in output.stdout.splitlines()
                    ],
                ))

        else:
            raise RunnerError(
                "libndt",
                "Executable libndt-client does not exist, please install libndt.",
            )
        return [json]
