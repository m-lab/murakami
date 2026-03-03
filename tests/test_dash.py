import json
from unittest.mock import Mock, patch
from murakami.runners.dash import DashClient


# Simulated dash-client JSON output (one line per segment)
MOCK_DASH_OUTPUT = "\n".join([
    json.dumps({"ServerURL": "https://dash.example.com", "Rate": 1000, "Elapsed": 1.2, "Received": 150000, "Connect": 0.05}),
    json.dumps({"ServerURL": "https://dash.example.com", "Rate": 1200, "Elapsed": 1.1, "Received": 160000, "Connect": 0.05}),
    json.dumps({"ServerURL": "https://dash.example.com", "Rate": 1100, "Elapsed": 1.3, "Received": 155000, "Connect": 0.05}),
])


def test_dash_success():
    """Test DASH parser returns structured JSON on success."""
    mock_proc = Mock(returncode=0, stdout=MOCK_DASH_OUTPUT, stderr="")
    with patch("shutil.which", return_value="/usr/bin/dash-client"):
        with patch("subprocess.run", return_value=mock_proc):
            runner = DashClient(config={})
            output = json.loads(runner.start_test())

    assert output["TestName"] == "dash"
    assert output["TestStartTime"] is not None
    assert output["TestEndTime"] is not None
    assert output["ServerURL"] == "https://dash.example.com"
    assert output["DownloadSpeed"] == sum([1000, 1200, 1100]) / 3
    assert output["DownloadSpeedUnit"] == "kbit/s"
    assert output["NumSegments"] == 3
    assert output["SegmentRates"] == [1000, 1200, 1100]
    assert output["Latency"] == 0.05


def test_dash_failure():
    """Test DASH parser returns error fields on failure."""
    mock_proc = Mock(returncode=1, stdout="", stderr="connection refused")
    with patch("shutil.which", return_value="/usr/bin/dash-client"):
        with patch("subprocess.run", return_value=mock_proc):
            runner = DashClient(config={})
            output = json.loads(runner.start_test())

    assert output["TestName"] == "dash"
    assert output["TestError"] == "connection refused"
    assert output["DownloadSpeed"] is None
    assert output["ServerURL"] is None


def test_dash_not_installed():
    """Test DASH raises RunnerError if dash-client is not installed."""
    from murakami.errors import RunnerError
    with patch("shutil.which", return_value=None):
        runner = DashClient(config={})
        try:
            runner.start_test()
            assert False, "Expected RunnerError"
        except RunnerError:
            pass


def test_dash_empty_output():
    """Test DASH parser handles empty output gracefully."""
    mock_proc = Mock(returncode=0, stdout="", stderr="")
    with patch("shutil.which", return_value="/usr/bin/dash-client"):
        with patch("subprocess.run", return_value=mock_proc):
            runner = DashClient(config={})
            output = json.loads(runner.start_test())

    assert output["TestError"] == "No segments parsed from output."
    assert output["DownloadSpeed"] is None
