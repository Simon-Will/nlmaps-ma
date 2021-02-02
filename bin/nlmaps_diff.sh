#!/usr/bin/env bash

NL="$1"
GOLD_MRL="$2"
SYS1_MRL="$3"
SYS2_MRL="$4"

if [ "$#" -lt 4 ]; then
    echo 'Usage: nlmaps_diff.sh nl_file gold_mrl_file sys1_mrl_file sys2_mrl_file'
    exit 1
fi

paste "$NL" "$GOLD_MRL" "$SYS1_MRL" "$SYS2_MRL" | \
    awk 'BEGIN { FS="\t"; OFS="\n"; ORS="\n\n"; } $3 != $4 { print $1, $2, $3, $4; }'
