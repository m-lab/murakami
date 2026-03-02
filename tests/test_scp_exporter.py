import base64
import os
from unittest.mock import MagicMock, patch

from murakami.exporters.scp import SCPExporter

FAKE_PEM = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA\n-----END RSA PRIVATE KEY-----\n"
FAKE_KEY_CONTENT = base64.b64encode(FAKE_PEM).decode("utf-8")


@patch("murakami.exporters.scp.SCPClient")
@patch("murakami.exporters.scp.SSHClient")
def test_scp_key_content_writes_temp_file(mock_ssh_cls, mock_scp_cls):
    """When key_content is in the config, the exporter decodes the base64 PEM,
    writes it to a temporary file (mode 0o600), passes that path to
    ssh.connect(), and deletes the file when done."""
    mock_ssh = MagicMock()
    mock_ssh_cls.return_value = mock_ssh
    mock_ssh.get_transport.return_value = MagicMock()

    mock_scp_instance = MagicMock()
    mock_scp_cls.return_value.__enter__ = MagicMock(return_value=mock_scp_instance)
    mock_scp_cls.return_value.__exit__ = MagicMock(return_value=False)

    exporter = SCPExporter(
        name="test",
        config={
            "target": "host:/remote/path",
            "username": "user",
            "key_content": FAKE_KEY_CONTENT,
        },
    )
    exporter._push_single(test_name="ndt7", data='{"result": 1}',
                           timestamp="2024-01-01T00:00:00.000000")

    connect_kwargs = mock_ssh.connect.call_args
    key_filename = connect_kwargs[1]["key_filename"]
    assert key_filename is not None, "key_filename should be set when key_content is provided"
    assert not os.path.exists(key_filename), "temp file must be deleted after push"


@patch("murakami.exporters.scp.SCPClient")
@patch("murakami.exporters.scp.SSHClient")
def test_scp_key_file_used_when_no_key_content(mock_ssh_cls, mock_scp_cls):
    """When key_content is absent, the exporter uses the file path from the
    key config option directly as key_filename."""
    mock_ssh = MagicMock()
    mock_ssh_cls.return_value = mock_ssh
    mock_ssh.get_transport.return_value = MagicMock()

    mock_scp_instance = MagicMock()
    mock_scp_cls.return_value.__enter__ = MagicMock(return_value=mock_scp_instance)
    mock_scp_cls.return_value.__exit__ = MagicMock(return_value=False)

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
