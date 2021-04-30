#!/usr/bin/env python3

import argparse
import json
import sys

import pyparsing as pp

from nlmaps_tools.parse_mrl import MrlGrammar


def parse_mrls(mrl_file):
    grammar = MrlGrammar()
    features = []
    with open(mrl_file) as f:
        for line in f:
            try:
                parse_result = grammar.parseMrl(line.strip(), is_escaped=False)
                features.append(parse_result['features'])
            except pp.ParseException:
                features.append(None)
    return features


def get_type(features):
    if features['query_type'] == 'dist':
        if len(features['sub']) == 1:
            return 'dist_closest'
        return 'dist_between'
    return features['query_type']


def get_from_features(features, key):
    if features['query_type'] == 'dist':
        return features['sub'][0].get(key)
    return features.get(key)


def get_area_error(sysf, goldf):
    sys_main_area = get_from_features(sysf, 'area')
    gold_main_area = get_from_features(goldf, 'area')
    if sys_main_area != gold_main_area:
        return True

    if (sysf['structure'] == 'dist_between'
            and goldf['structure'] == 'dist_between'):
        if sysf['sub'][1].get('area') != goldf['sub'][1].get('area'):
            return True

    return False


def get_center_nwr_error(sysf, goldf):
    sys_center_nwr = get_from_features(sysf, 'center_nwr')
    gold_center_nwr = get_from_features(goldf, 'center_nwr')
    return bool(sys_center_nwr and gold_center_nwr
            and sys_center_nwr != gold_center_nwr)


def get_target_nwr_error(sysf, goldf):
    sys_main_target_nwr = get_from_features(sysf, 'target_nwr')
    gold_main_target_nwr = get_from_features(goldf, 'target_nwr')
    if sys_main_target_nwr != gold_main_target_nwr:
        return True

    if (sysf['structure'] == 'dist_between'
            and goldf['structure'] == 'dist_between'):
        if (sysf['sub'][1].get('target_nwr')
                != goldf['sub'][1].get('target_nwr')):
            return True

    return False


def get_maxdist_error(sysf, goldf):
    sys_maxdist = get_from_features(sysf, 'maxdist')
    gold_maxdist = get_from_features(goldf, 'maxdist')
    return bool(sys_maxdist and gold_maxdist and sys_maxdist != gold_maxdist)


def get_around_topx_error(sysf, goldf):
    sys_maxdist = get_from_features(sysf, 'around_topx')
    gold_maxdist = get_from_features(goldf, 'around_topx')
    if (goldf['query_type'] == 'around_query'
            and sysf['query_type'] == 'around_query'):
        return sys_maxdist != gold_maxdist
    return False


def get_qtype_error(sysf, goldf):
    if (sysf['query_type'] in ('in_query', 'around_query')
            and goldf['query_type'] in ('in_query', 'around_query')):
        return sysf.get('qtype') != goldf.get('qtype')
    return False


def main(system_mrls, gold_mrls):
    sys_features = parse_mrls(system_mrls)
    gold_features = parse_mrls(gold_mrls)

    error_classifications = []

    for sysf, goldf in zip(sys_features, gold_features):
        if not sysf or not goldf:
            error_classifications.append({
                'structure': True,
                'area': False, 'center_nwr': False, 'target_nwr': False,
                'maxdist': False, 'around_topx': False, 'qtype': False,
                'other': False
            })
            continue

        sys_type = get_type(sysf)
        gold_type = get_type(goldf)
        sysf['structure'] = sys_type
        goldf['structure'] = gold_type

        errors = {
            'structure': sys_type != gold_type,
            'area': get_area_error(sysf, goldf),
            'center_nwr': get_center_nwr_error(sysf, goldf),
            'target_nwr': get_target_nwr_error(sysf, goldf),
            'maxdist': get_maxdist_error(sysf, goldf),
            'around_topx': get_around_topx_error(sysf, goldf),
            'qtype': get_qtype_error(sysf, goldf),
            'other': False,
        }
        if not any(errors.values()) and sysf != goldf:
            print(sysf, file=sys.stderr)
            print(goldf, file=sys.stderr)
            print('----------', file=sys.stderr)
            errors['other'] = True
        error_classifications.append(errors)


    print(json.dumps(error_classifications, indent=2))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('system_mrls')
    parser.add_argument('gold_mrls')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
