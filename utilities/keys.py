import os
import base64
from pathlib import Path
from typing import Union

class KeyLoadError(Exception):
    """Raised when a key fails to load from env or file."""

def load_key(
    env_var: str,
    file_path: Union[str, Path]
) -> bytes:
    """
    Load a key from an environment variable or fallback file path.

    Environment variable content must be **base64 encoded**.
    If env var is not set, fallback to reading the file path directly.

    Raises:
        KeyLoadError: if neither source is available or decode fails.
    """

    # Try environment variable first
    key_b64 = os.environ.get(env_var)
    if key_b64:
        try:
            return base64.b64decode(key_b64.encode("utf-8"))
        except Exception as exc:
            raise KeyLoadError(
                f"Failed to decode {env_var} as base64: {exc}"
            )

    # Fallback to file on disk
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as exc:
        raise KeyLoadError(
            f"Could not load key from env {env_var} or file {file_path}: {exc}"
        )
