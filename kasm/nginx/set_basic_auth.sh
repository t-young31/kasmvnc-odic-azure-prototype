#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sed 's/{{ basic-auth }}/'"$1"'/g' "$SCRIPT_DIR/nginx.conf.template" > "$SCRIPT_DIR/nginx.conf"
