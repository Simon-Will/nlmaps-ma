#!/usr/bin/env python3

import argparse
from collections import Counter
import sys

from nlmaps_tools.parse_mrl import MrlGrammar


def get_areas_from_features(features):
    if features['query_type'] == 'dist':
        features_list = features['sub']
    else:
        features_list = [features]

    areas = []
    for f in features_list:
        area = f.get('area')
        if area:
            areas.append(area)

    return areas


def main(mrl_files):
    grammar = MrlGrammar()
    areas = []
    for filename in mrl_files:
        print('Parsing mrls in {} …'.format(filename), file=sys.stderr)
        with open(filename) as f:
            for line in f:
                mrl = line.strip()
                parse_result = grammar.parseMrl(mrl, is_escaped=False)
                features = parse_result['features']
                areas.extend(get_areas_from_features(features))

    counts = Counter(areas)
    for area, count in sorted(counts.items(), key=lambda item: item[1]):
        print('{}\t{}'.format(area, count))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mrl_files', nargs='+')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
