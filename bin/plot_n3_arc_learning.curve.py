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


def main(validations_file, outfile):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    steps, accuracies = read_scores(validations_file, 'main')
    plot_curve(ax, steps, accuracies, label=r'Accuracy on v4 Dev')
    start_accuracy = accuracies[0]

    steps, accuracies = read_scores(validations_file, 'valid2')
    plot_curve(ax, steps, accuracies, label=r'Accuracy on v3 Dev')

    xmin, xmax = steps[0], steps[-1]
    ax.hlines([start_accuracy], xmin, xmax, colors='gray',
              linestyles='dotted', label=r'Starting Accuracy on NLMaps\,v4 Dev')

    ax.legend()
    ax.set_ylim(0, 100)
    ax.set_xlim(xmin, xmax)
    ax.set_xlabel('Steps')
    ax.set_ylabel('Accuracy')
    plt.tight_layout()

    fig.savefig(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('validations_file')
    parser.add_argument('outfile')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
