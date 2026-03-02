#!/bin/sh
# Encode a key file for use with Murakami's GCS or SCP exporter.
#
# Usage:
#   encode_key.sh /path/to/sa.json     (GCS service account JSON)
#   encode_key.sh /path/to/id_rsa      (SCP PEM private key)
#
# The encoded value is read by Murakami's existing environment variable
# config mechanism (load_env in __main__.py).  Set it as:
#
#   GCS exporter (in murakami.toml or as env var):
#     [exporters.gcs]
#     key_content = "<encoded value>"
#   Or via environment variable:
#     export MURAKAMI_EXPORTERS_GCS_KEY_CONTENT="<encoded value>"
#
#   SCP exporter:
#     [exporters.scp]
#     key_content = "<encoded value>"
#   Or via environment variable:
#     export MURAKAMI_EXPORTERS_SCP_KEY_CONTENT="<encoded value>"

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/keyfile" >&2
    exit 1
fi

base64 -w 0 "$1"
echo ""
