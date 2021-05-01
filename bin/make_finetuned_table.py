#!/usr/bin/env python3

from collections import OrderedDict
import json
import sys


MODEL_MAPPING = OrderedDict((
    ('n3.yaml', r'\nlmthree{}'),
    ('n3_arc.yaml', r'\nlmthree{} \textrightarrow{} \nlmfour{}'),
    ('n3_arc_ratio05.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{}'),
    ('n3_arc_adadelta_1-0-0.yaml', r'\nlmthree{} \textrightarrow{} \nlmfour{} Adadelta 1-0-0 Iter: 1'),
    ('n3_arc_adadelta_1-0-5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adadelta 1-0-5 Iter: 1'),
    ('n3_arc_adadelta_1-4-5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adadelta 1-4-5 Iter: 1'),
    ('n3_arc_adadelta_1-4-5_5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adadelta 1-4-5 Iter: 5'),
    ('n3_arc_adam_1-0-0.yaml', r'\nlmthree{} \textrightarrow{} \nlmfour{} Adam 1-0-0 Iter: 1'),
    ('n3_arc_adam_1-0-5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adam 1-0-5 Iter: 1'),
    ('n3_arc_adam_1-4-5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adam 1-4-5 Iter: 1'),
    ('n3_arc_adam_1-4-5_5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfour{} Adam 1-4-5 Iter: 5'),
    ('n3_ar_adam_1-4-5.yaml', r'\nlmthree{} \textrightarrow{} \nlmthree{}/\nlmfourraw{} Adam 1-4-5 Iter: 1')
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
    #'nlmaps_v2/split_1_train_dev_test/nlmaps.v2.test',
    'nlmaps_v2delta/nlmaps.v2.test',
    #'nlmaps_v3epsilon/v3epsilon.normal/nlmaps.v3epsilon.test',
    #'nlmaps_v3epsilon/v3epsilon.noise/nlmaps.v3epsilon.test',
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
