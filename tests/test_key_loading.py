import os
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from utilities.keys import load_key, KeyLoadError
from murakami.exporters.gcs import GCSExporter
from murakami.exporters.scp import SCPExporter


def create_dummy_file(content: bytes, tmp_path: Path, filename: str) -> str:
    """
    Write bytes to a file and return its path as a string.
    """
    path = tmp_path / filename
    path.write_bytes(content)
    return str(path)


# Tests for GCSExporter fallback
def test_gcs_key_fallback(tmp_path: Path, monkeypatch):
    """
    GCSExporter should load key file; mock storage.Client to avoid real PEM parsing.
    """
    key_file = tmp_path / "gcs.json"
    # Minimal GCS JSON to trigger loading
    key_file.write_text(json.dumps({"type": "service_account"}))

    # Ensure environment variable is not set
    monkeypatch.delenv("MURAKAMI_EXPORTERS_GCS_KEY", raising=False)

    with patch("murakami.exporters.gcs.storage.Client.from_service_account_json") as MockClient:
        exporter = GCSExporter(config={"key": key_file, "target": "dummy"})
        # Assert that the exporter attempted to load the key
        MockClient.assert_called_once()



# Tests for SCPExporter fallback
def test_scp_key_fallback(tmp_path: Path, monkeypatch):
    """
    SCPExporter should correctly read private key bytes from file.
    """
    key_content = b"private-key-data"
    key_file = create_dummy_file(key_content, tmp_path, "scp.key")

    monkeypatch.delenv("MURAKAMI_EXPORTERS_SCP_KEY", raising=False)
    exporter = SCPExporter(config={"key": key_file, "target": "host:/tmp"})

    # Handle Path, str, or bytes
    if isinstance(exporter.private_key, Path):
        actual_key = exporter.private_key.read_bytes()
    elif isinstance(exporter.private_key, str):
        actual_key = Path(exporter.private_key).read_bytes()
    else:
        actual_key = exporter.private_key

    assert actual_key == key_content



# Tests for load_key utility
def test_load_key_from_env(monkeypatch):
    """
    Should load bytes from environment variable (base64 encoded).
    """
    import base64

    secret = b"env-secret"
    monkeypatch.setenv("MY_KEY_ENV", base64.b64encode(secret).decode("utf-8"))

    loaded = load_key("MY_KEY_ENV", "unused_path")
    assert loaded == secret


def test_load_key_from_file(tmp_path: Path, monkeypatch):
    """
    Should load bytes from fallback file when env var not set.
    """
    content = b"file-secret"
    file_path = tmp_path / "keyfile"
    file_path.write_bytes(content)

    monkeypatch.delenv("MY_KEY_ENV", raising=False)
    loaded = load_key("MY_KEY_ENV", file_path)
    assert loaded == content


def test_load_key_missing(monkeypatch):
    """
    Should raise KeyLoadError when neither environment variable nor file exists.
    """
    monkeypatch.delenv("MY_KEY_ENV", raising=False)
    with pytest.raises(KeyLoadError):
        load_key("MY_KEY_ENV", None)