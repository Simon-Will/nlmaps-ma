#!/usr/bin/env python3

import argparse
import os
import re

import matplotlib
matplotlib.use('pgf')
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": ["Linux Libertine O"],
    "font.sans-serif": ["Linux Libertine O"],
}
matplotlib.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pyplot as plt


MODEL_TO_DEV_LABEL = {
    'n21': 'valid2',
    'n3a': 'valid2',
    'n3b': 'valid2',
    'n3': 'valid2',
    'n3normal': 'valid2',
}


MODEL_TO_LEGEND_LABEL = {
    'n21': 'Trained on v2.1',
    'n3a': 'Trained on v3a',
    'n3b': 'Trained on v3b',
    'n3': 'Trained on v3',
    'n3normal': r'Trained on v3$_{\textrm{no-noise}}$',
}


def get_field(line, field):
    regex = re.escape(field) + r': ([\d.]+)'
    match = re.search(regex, line)
    if not match:
        raise ValueError('No match for {} in line {}'.format(regex, line))
    value = match.group(1)

    if '.' in value:
        value = float(value)
    else:
        value = int(value)
    return value


def read_scores(path, label):
    steps, accuracies = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith(label):
                continue
            step = get_field(line, 'Steps')
            accuracy = get_field(line, 'sequence_accuracy')
            steps.append(step)
            accuracies.append(accuracy)

    return steps, accuracies


def plot_curve(ax, steps, accuracies, **kwargs):
    ax.plot(steps, accuracies, **kwargs)


def main(validations_dir, outfile):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for model, label in MODEL_TO_DEV_LABEL.items():
        path = os.path.join(validations_dir, model, 'validations.txt')
        steps, accuracies = read_scores(path, label)
        legend_label = MODEL_TO_LEGEND_LABEL[model]
        plot_curve(ax, steps, accuracies, label=legend_label)

    ax.legend()
    #ax.set_xlim(0, 200)
    #ax.set_ylim(0.55, 0.7)
    ax.set_xlabel('Steps')
    ax.set_ylabel('NLMaps\,v3 Dev Accuracy')
    plt.tight_layout()

    fig.savefig(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('validations_dir')
    parser.add_argument('outfile')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
