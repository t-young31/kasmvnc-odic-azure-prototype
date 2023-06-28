#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ENV_FILEPATH="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILEPATH" ]; then  # if a .env file exits
    echo "$ENV_FILEPATH not found. Please create it from .env.sample"
    exit 1
fi

echo "Exporting variables in .env file into environment"
read -ra args < <(grep -v '^#' "$ENV_FILEPATH" | xargs)
export "${args[@]}"

# Add a cookie secret if one it not set
if [ -z "${COOKIE_SECRET+x}" ]; then
    COOKIE_SECRET_VALUE=$(python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())')
    echo "COOKIE_SECRET=$COOKIE_SECRET_VALUE" >> .env
    export COOKIE_SECRET="$COOKIE_SECRET_VALUE"
fi
