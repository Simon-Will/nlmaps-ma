#!/usr/bin/env bash

#THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
#LOCAL_TOP_DIR="$THIS_DIR/../validations"
LOCAL_TOP_DIR=~/ma/nlmaps-ma/validations

REMOTE_HOST=cluster
REMOTE_TOP_DIR='~/ma/joeynmt/models'

ssh "$REMOTE_HOST" find "$REMOTE_TOP_DIR" -name validations.txt \
    | while read -r path; do
    model=$(basename "$(dirname "$path")")
    dest=$LOCAL_TOP_DIR/$model/validations.txt
    mkdir -p "$(dirname "$dest")"
    scp "$REMOTE_HOST:$path" "$dest"
done
