#!/usr/bin/env python3

import argparse
from collections import defaultdict
import itertools
import json
import re
import sys

from nlmaps_tools.answer_mrl import canonicalize_nwr_features
from nlmaps_tools.parse_mrl import MrlGrammar

TAGS = [
    ('sport', 'cricket'),
    ('shop', 'butcher'),
    ('generator:source', 'wind'),
    ('building', '*'),
    ('leisure', 'dog_park'),
    ('tourism', 'gallery'),
    ('amenity', 'bank'),
    ('cuisine', 'mexican'),
    ('landuse', 'farm'),
    ('amenity', 'fire_station'),
    ('amenity', 'courthouse'),
    ('sport', 'ice_skating'),
    ('healthcare', 'optometrist'),
    ('brand:wikidata', 'Q177054'),
    ('amenity', 'bus_station'),
    ('man_made', 'adit'),
    ('sport', 'equestrian'),
    ('sport', 'basketball'),
    ('denomination', 'roman_catholic'),
    ('shop', 'tattoo'),
]

def get_tags_in_nwr(nwr, exclude=tuple()):
    nwr = canonicalize_nwr_features(nwr)
    tags = []
    for feat in nwr:
        if feat[0] in ['or', 'and'] and isinstance(feat[1], (list, tuple)):
            for key, val in feat[1:]:
                if key not in exclude:
                    tags.append((key, val))
        elif len(feat) == 2 and all(isinstance(f, str) for f in feat):
            if feat[0] not in exclude:
                tags.append((feat[0], feat[1]))
        else:
            raise ValueError('Unexpected feature part: {}'.format(feat))
    return tags


def get_tags_in_features(features, exclude=tuple()):
    if 'sub' in features:
        tags = list(itertools.chain.from_iterable(
            get_tags_in_features(feats)
            for feats in features['sub']
            if feats
        ))
        return tags

    tags = get_tags_in_nwr(features['target_nwr'], exclude=exclude)
    if 'center_nwr' in features:
        tags.extend(get_tags_in_nwr(features['center_nwr'], exclude=exclude))

    return tags


def read_mrls(filename):
    mrls = []
    with open(filename) as f:
        for line in f:
            mrl = line.strip()
            mrls.append(mrl)
    return mrls


def is_present(tag, mrl):
    if not mrl:
        return False

    key_regex = re.escape(tag[0])
    val_regex = re.escape(tag[1])
    regex = r"keyval\('{}[^\)]+{}".format(key_regex, val_regex)
    match = re.search(regex, mrl)
    return bool(match)


def main(gold_mrl_file, sys_mrl_file, outfile):
    gold_mrls = read_mrls(gold_mrl_file)
    sys_mrls = read_mrls(sys_mrl_file)

    analysis = defaultdict(list)

    for idx, (gmrl, smrl) in enumerate(zip(gold_mrls, sys_mrls), 1):
        for tag in TAGS:
            if is_present(tag, gmrl):
                formatted_tag = '{}={}'.format(tag[0], tag[1])
                if gmrl == smrl:
                    analysis[formatted_tag].append((idx, 'correct'))
                elif is_present(tag, smrl):
                    analysis[formatted_tag].append((idx, 'tag_present'))
                else:
                    analysis[formatted_tag].append((idx, 'tag_missing'))

    with open(outfile, 'w') as f:
        json.dump(analysis, f, indent=2)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('gold_mrl_file')
    parser.add_argument('sys_mrl_file')
    parser.add_argument('outfile')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
