import json
from unittest.mock import Mock, patch

from murakami.runners.ndt7 import Ndt7Client


def test_ndt7_upload_uses_upload_throughput():
    summary = {
        "ServerFQDN": "server.example",
        "ServerIP": "203.0.113.1",
        "ClientIP": "198.51.100.2",
        "Download": {
            "UUID": "download-uuid",
            "Throughput": {"Value": 1, "Unit": "bps"},
        },
        "Upload": {
            "Throughput": {"Value": 2, "Unit": "bps"},
        },
    }

    mock_proc = Mock(returncode=0, stdout=json.dumps(summary))

    with patch("shutil.which", return_value="/usr/bin/ndt7-client"):
        with patch("subprocess.run", return_value=mock_proc):
            runner = Ndt7Client(config={})
            output = json.loads(runner.start_test())

    assert output["DownloadValue"] == 1
    assert output["UploadValue"] == 2
