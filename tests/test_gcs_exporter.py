import base64
import json
import os
from unittest.mock import MagicMock, patch


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
def test_gcs_env_var_uses_from_service_account_info(mock_client_cls):
    mock_client_cls.from_service_account_info.return_value = MagicMock()

    env = {"MURAKAMI_GCS_KEY_CONTENT": FAKE_KEY_CONTENT}
    with patch.dict(os.environ, env, clear=False):
        from murakami.exporters.gcs import GCSExporter
        exporter = GCSExporter(
            name="test",
            config={"target": "gs://bucket/path"},
        )

    mock_client_cls.from_service_account_info.assert_called_once_with(
        FAKE_KEY_DICT
    )
    mock_client_cls.from_service_account_json.assert_not_called()


@patch("murakami.exporters.gcs.storage.Client")
def test_gcs_file_path_used_when_no_env_var(mock_client_cls):
    mock_client_cls.from_service_account_json.return_value = MagicMock()

    env_without_var = {k: v for k, v in os.environ.items()
                       if k != "MURAKAMI_GCS_KEY_CONTENT"}
    with patch.dict(os.environ, env_without_var, clear=True):
        from murakami.exporters.gcs import GCSExporter
        exporter = GCSExporter(
            name="test",
            config={"target": "gs://bucket/path", "key": "/path/to/key.json"},
        )

    mock_client_cls.from_service_account_json.assert_called_once_with(
        "/path/to/key.json"
    )
    mock_client_cls.from_service_account_info.assert_not_called()
