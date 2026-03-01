#!/bin/sh
# Usage: encode_key.sh /path/to/key.json   (GCS service account JSON)
#        encode_key.sh /path/to/id_rsa      (SCP PEM private key)
#
# The encoded value can then be exported as:
#   export MURAKAMI_GCS_KEY_CONTENT="<output>"   # for the GCS exporter
#   export MURAKAMI_SCP_KEY_CONTENT="<output>"   # for the SCP exporter

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/keyfile" >&2
    exit 1
fi

encoded=$(base64 -w 0 "$1")
echo "$encoded"
echo ""
echo "Set the above value as MURAKAMI_GCS_KEY_CONTENT or MURAKAMI_SCP_KEY_CONTENT"
echo "in your environment or container configuration."
