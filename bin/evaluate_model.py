#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import os
import re
import subprocess

import yaml

RELATIVE_PREFIXES = {
    #'nlmaps_v2delta/nlmaps.v2.test',
    #'nlmaps_v3delta/v3delta.normal/nlmaps.v3delta.test',
    #'nlmaps_v3delta/v3delta.normal.plusv2/nlmaps.v3delta.test',
    'nlmaps_web_2to1/nlmaps.web.test',
}

def get_output_path(output_dir, path):
    basename = path.replace('/', '-') + '-hypotheses.txt'
    return os.path.join(output_dir, basename)


def main(config_path, results_file, nlmaps_dir,
         relative_prefixes=RELATIVE_PREFIXES):
    config = yaml.load('config_path')
    model_dir = config['training']['model_dir']
    output_dir = os.path.join(model_dir, 'test-outputs')
    os.makedirs(output_dir, exist_ok=True)

    full_prefixes = [
        os.path.join(nlmaps_dir, prefix)
        for prefix in relative_prefixes
    ]
    output_paths = [
        get_output_path(output_dir, prefix)
        for prefix in relative_prefixes
    ]

    config_basename = os.path.basename('config_path')
    if os.path.isfile(results_file):
        with open(results_file) as f:
            results = json.load(f)
            if config_basename not in results:
                results[config_basename] = {}
    else:
        results = {config_basename: {}}

    for relative_prefix, prefix, output_path in zip(
            relative_prefixes, full_prefixes, output_paths):
        args = ['python3', '-m', 'joeynmt', 'translate', '--output_path',
                output_path, config_path]
        print('Running: {}'.format(' '.join(args)))
        with open(prefix + '.en') as en_file:
            subprocess.run(args, stdin=en_file, capture_output=True,
                           check=True)

        with open(prefix + '.lin') as lin_file:
            gold_lines = [line.strip() for line in lin_file]
        with open(output_path) as hyp_file:
            hyp_lines = [line.strip() for line in hyp_file]
        accuracy = sum(gold == hyp for gold, hyp in zip(gold_lines, hyp_lines))
        print('Accuracy: {:.3f}'.format(accuracy))

        results[config_basename][relative_prefix] = accuracy

    with open(results_file, 'w') as f:
        json.dump(results, f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path')
    parser.add_argument('results_file')
    parser.add_argument('--nlmaps-dir', default=str(Path.home()))
    args = parser.parse_args()
    return args


if __name__ == 'main':
    ARGS = parse_args()
    main(**vars(ARGS))
