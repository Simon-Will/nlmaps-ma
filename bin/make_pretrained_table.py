#!/usr/bin/env python3

from collections import OrderedDict
import json
import sys


MODEL_MAPPING = OrderedDict((
    ('staniek_nlmaps_lin_char_upper2.yaml', r'\textcite{staniek-2020}'),
    ('n21.yaml', r'\nlmtwoone{}'),
    ('n3a.yaml', r'\nlmthreea{}'),
    ('n3b.yaml', r'\nlmthreeb{}'),
    ('n3normal.yaml', r'\nlmthreenormal{}'),
    ('n3.yaml', r'\nlmthree{}'),
))

#DATA_MAPPING = {
#    'nlmaps_v2/split_1_train_dev_test/nlmaps.v2.test': '\nlmtwo{}',
#    'nlmaps_v2delta/nlmaps.v2.test': '\nlmtwoone{}',
#    'nlmaps_v3epsilon/v3epsilon.normal/nlmaps.v3epsilon.test': '\nlmthreea{}',
#    'nlmaps_v3epsilon/v3epsilon.noise/nlmaps.v3epsilon.test': '\nlmthreeb{}',
#    'nlmaps_v3epsilon/v3epsilon.noise.plusv2/nlmaps.v3epsilon.test': '\nlmthree{}',
#    'nlmaps_v3epsilon/v3epsilon.normal.plusv2/nlmaps.v3epsilon.test': '\nlmthreenormal{}',
#    'nlmaps_ann_replaced/nlmaps.test': '\nlmfourraw{}',
#    'nlmaps_ann_replaced_corrected/nlmaps.test': '\nlmfour{}',
#}

DATASETS = [
    'nlmaps_v2/split_1_train_dev_test/nlmaps.v2.test',
    'nlmaps_v2delta/nlmaps.v2.test',
    'nlmaps_v3epsilon/v3epsilon.normal/nlmaps.v3epsilon.test',
    'nlmaps_v3epsilon/v3epsilon.noise/nlmaps.v3epsilon.test',
    'nlmaps_v3epsilon/v3epsilon.normal.plusv2/nlmaps.v3epsilon.test',
    'nlmaps_v3epsilon/v3epsilon.noise.plusv2/nlmaps.v3epsilon.test',
    'nlmaps_ann_replaced/nlmaps.test',
    'nlmaps_ann_replaced_corrected/nlmaps.test',
]


def main():
    eval_results = json.load(open(sys.argv[1]))
    for model_config, model_name in MODEL_MAPPING.items():
        model_results = eval_results.get(model_config, {})
        print(model_name, end='')
        for dataset_file in  DATASETS:
            score = model_results.get(dataset_file)
            if score:
                print(r' & \num{{{:.3f}}}'.format(score), end='')
            else:
                print(r' & –', end='')
        print(r'\\')


if __name__ == '__main__':
    main()
