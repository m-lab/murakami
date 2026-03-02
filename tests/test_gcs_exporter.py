import base64
import json
from unittest.mock import MagicMock, patch

from murakami.exporters.gcs import GCSExporter

FAKE_KEY_DICT = {
    "type": "service_account",
    "project_id": "test-project",
    "private_key_id": "key-id",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA\n-----END RSA PRIVATE KEY-----\n",
    "client_email": "test@test-project.iam.gserviceaccount.com",
    "client_id": "123456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
}

FAKE_KEY_CONTENT = base64.b64encode(
    json.dumps(FAKE_KEY_DICT).encode("utf-8")
).decode("utf-8")


@patch("murakami.exporters.gcs.storage.Client")
def test_gcs_key_content_uses_from_service_account_info(mock_client_cls):
    """When key_content is in the config, credentials are loaded from inline
    base64-encoded JSON rather than a file on disk."""
    mock_client_cls.from_service_account_info.return_value = MagicMock()

    GCSExporter(
        name="test",
        config={"target": "gs://bucket/path", "key_content": FAKE_KEY_CONTENT},
    )

    mock_client_cls.from_service_account_info.assert_called_once_with(FAKE_KEY_DICT)
    mock_client_cls.from_service_account_json.assert_not_called()


@patch("murakami.exporters.gcs.storage.Client")
def test_gcs_key_file_used_when_no_key_content(mock_client_cls):
    """When key_content is absent, the exporter falls back to reading
    credentials from the file path given by the key config option."""
    mock_client_cls.from_service_account_json.return_value = MagicMock()

    GCSExporter(
        name="test",
        config={"target": "gs://bucket/path", "key": "/path/to/key.json"},
    )

    mock_client_cls.from_service_account_json.assert_called_once_with("/path/to/key.json")
    mock_client_cls.from_service_account_info.assert_not_called()
