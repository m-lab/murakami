import base64
import os
from unittest.mock import MagicMock, call, patch


FAKE_PEM = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA\n-----END RSA PRIVATE KEY-----\n"
FAKE_KEY_CONTENT = base64.b64encode(FAKE_PEM).decode("utf-8")


@patch("murakami.exporters.scp.SCPClient")
@patch("murakami.exporters.scp.SSHClient")
def test_scp_env_var_writes_temp_file(mock_ssh_cls, mock_scp_cls):
    mock_ssh = MagicMock()
    mock_ssh_cls.return_value = mock_ssh
    mock_ssh.get_transport.return_value = MagicMock()

    mock_scp_instance = MagicMock()
    mock_scp_cls.return_value.__enter__ = MagicMock(return_value=mock_scp_instance)
    mock_scp_cls.return_value.__exit__ = MagicMock(return_value=False)

    env = {"MURAKAMI_SCP_KEY_CONTENT": FAKE_KEY_CONTENT}
    with patch.dict(os.environ, env, clear=False):
        from murakami.exporters.scp import SCPExporter
        exporter = SCPExporter(
            name="test",
            config={
                "target": "host:/remote/path",
                "username": "user",
            },
        )
        exporter._push_single(test_name="ndt7", data='{"result": 1}',
                               timestamp="2024-01-01T00:00:00.000000")

    connect_kwargs = mock_ssh.connect.call_args
    key_filename = connect_kwargs[1]["key_filename"]
    assert key_filename is not None
    assert not os.path.exists(key_filename), "temp file must be deleted after push"


@patch("murakami.exporters.scp.SCPClient")
@patch("murakami.exporters.scp.SSHClient")
def test_scp_file_path_used_when_no_env_var(mock_ssh_cls, mock_scp_cls):
    mock_ssh = MagicMock()
    mock_ssh_cls.return_value = mock_ssh
    mock_ssh.get_transport.return_value = MagicMock()

    mock_scp_instance = MagicMock()
    mock_scp_cls.return_value.__enter__ = MagicMock(return_value=mock_scp_instance)
    mock_scp_cls.return_value.__exit__ = MagicMock(return_value=False)

    env_without_var = {k: v for k, v in os.environ.items()
                       if k != "MURAKAMI_SCP_KEY_CONTENT"}
    with patch.dict(os.environ, env_without_var, clear=True):
        from murakami.exporters.scp import SCPExporter
        exporter = SCPExporter(
            name="test",
            config={
                "target": "host:/remote/path",
                "username": "user",
                "key": "/path/to/id_rsa",
            },
        )
        exporter._push_single(test_name="ndt7", data='{"result": 1}',
                               timestamp="2024-01-01T00:00:00.000000")

    connect_kwargs = mock_ssh.connect.call_args
    assert connect_kwargs[1]["key_filename"] == "/path/to/id_rsa"
