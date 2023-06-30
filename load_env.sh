#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
env_filepath="$SCRIPT_DIR/.env"

if [ ! -f "$env_filepath" ]; then  # if a .env file exits
    echo "$env_filepath not found. Please create it from .env.sample"
    exit 1
fi

echo "Exporting variables in .env file into environment"
read -ra args < <(grep -v '^#' "$env_filepath" | xargs)
export "${args[@]}"

# Add a cookie secret if one it not set
if [ -z "${COOKIE_SECRET+x}" ]; then
    cookie_secret_value=$(python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())')
    echo "COOKIE_SECRET=$cookie_secret_value" >> .env
    export COOKIE_SECRET="$cookie_secret_value"
fi

# Create a random value for the kasm vm basic auth and set it
KASM_VM_PASSWORD=$(python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())')
kasm_basic_auth="Basic $(echo -n "kasm_user:$KASM_VM_PASSWORD" | base64)"
"$SCRIPT_DIR/kasm/nginx/set_basic_auth.sh" "$kasm_basic_auth"

export KASM_VM_PASSWORD
