#!/usr/bin/env python3

import argparse
from collections import Counter
import itertools
import sys

from nlmaps_tools.answer_mrl import canonicalize_nwr_features
from nlmaps_tools.parse_mrl import MrlGrammar


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


def main(mrl_files):
    grammar = MrlGrammar()
    counts = Counter()
    for filename in mrl_files:
        print('Parsing mrls in {} …'.format(filename), file=sys.stderr)
        with open(filename) as f:
            for line in f:
                mrl = line.strip()
                parse_result = grammar.parseMrl(mrl, is_escaped=False)
                features = parse_result['features']
                tags = get_tags_in_features(features)
                for tag in tags:
                    if tag[0] == 'name':
                        counts[tag[1]] += 1

    for name, count in sorted(counts.items(), key=lambda item: item[1]):
        print('{}\t{}'.format(name, count))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mrl_files', nargs='+')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
