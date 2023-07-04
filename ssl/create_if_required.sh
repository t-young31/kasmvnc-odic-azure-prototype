#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

KEY_FILEPATH="${SCRIPT_DIR}/${CERT_KEY_NAME}"
CERT_FILEPATH="${SCRIPT_DIR}/${CERT_CERTIFICATE_NAME}"

if [ -f "$KEY_FILEPATH" ] && [ -f "$CERT_FILEPATH" ]; then
  echo "Found key and cert. Not creating"
  exit 0
fi

set +u  # Allow unset variables

# Create a self-signed certificate with a 10 year expiry and no passphrase
openssl req -x509 \
  -newkey rsa:4096 \
  -keyout "$KEY_FILEPATH" \
  -out "$CERT_FILEPATH" \
  -sha256 \
  -days 3650 \
  -nodes \
  -subj "/C=GB/CN=localhost"
