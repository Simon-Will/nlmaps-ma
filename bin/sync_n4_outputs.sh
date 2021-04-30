#!/usr/bin/env bash

#THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
#LOCAL_TOP_DIR="$THIS_DIR/../validations"
LOCAL_TOP_DIR=~/ma/nlmaps-ma/n4_outputs

REMOTE_HOST=cluster
REMOTE_TOP_DIR='~/ma/joeynmt/models'
REMOTE_BASENAME=nlmaps_ann_replaced_corrected-nlmaps.test-hypotheses.txt

ssh "$REMOTE_HOST" find "$REMOTE_TOP_DIR" -name "$REMOTE_BASENAME" \
    | while read -r path; do
    model=$(basename "$(dirname "$(dirname "$path")")")
    dest="$LOCAL_TOP_DIR/$model/${REMOTE_BASENAME%txt}lin"
    echo "$model"
    mkdir -p "$(dirname "$dest")"
    scp "$REMOTE_HOST:$path" "$dest" >/dev/null
    python -m nlmaps_tools.mrl.functionalise -i "$dest" -o "${dest%lin}mrl"
done
