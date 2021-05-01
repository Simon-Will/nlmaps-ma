#!/usr/bin/env python3

import argparse
from collections import defaultdict, namedtuple
import re
import sys

import matplotlib
matplotlib.use('pgf')
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": ["Linux Libertine O"],
    "font.sans-serif": ["Linux Libertine O"],
}
matplotlib.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pyplot as plt

Record = namedtuple('Record', ('model', 'dataset', 'step', 'score'))


def format_model(model):
    match = re.match(r'n3_(arc?)_(adam|adadelta)_(\d-\d-\d)(_5)?\.yaml', model)
    if not match:
        print(model)
        sys.exit(1)

    dataset = r'v4$_{\textrm{raw}}$' if match.group(1) == 'ar' else 'v4'
    optimizer = match.group(2).title()
    config = match.group(3)
    iterations = 'Iter: 5' if match.group(4) else 'Iter: 1'

    return '{} {} {} {}'.format(dataset, optimizer, config, iterations)


def read_records(infile):
    records = defaultdict(list)
    with open(infile) as f:
        for line in f:
            model, dataset, step, correct, total = line.strip().split('|')
            model = format_model(model)
            score = 100 * int(correct) / int(total)
            records[(model, dataset)].append(
                Record(model, dataset, int(step), score)
            )
    return records


def plot_curve(ax, steps, accuracies, **kwargs):
    ax.plot(steps, accuracies, **kwargs)


def main(online_csv, dataset_to_plot, outfile, ylabel, best_accuracy):

    records_by_model = read_records(online_csv)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for (model, dataset), records in records_by_model.items():
        if dataset == dataset_to_plot:
            steps = [r.step for r in records]
            scores = [r.score for r in records]
            plot_curve(ax, steps, scores, label=model)

    start_accuracy = scores[0]
    xmin, xmax = steps[0], steps[-1]

    ax.hlines([start_accuracy], xmin, xmax, colors='gray',
              linestyles='dotted', label=r'Starting Accuracy')

    if best_accuracy:
        ax.hlines([best_accuracy], xmin, xmax, colors='gray',
                  linestyles='dashed', label='Top Accuracy of Offline Training')

    if dataset_to_plot == 'dev':
        ymin, ymax = 30, 62
    else:
        ymin, ymax = 50, 90

    ax.legend()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Steps')
    ax.set_ylabel(ylabel)
    fig.tight_layout()

    fig.savefig(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('online_csv')
    parser.add_argument('outfile')
    parser.add_argument('--ylabel', '-y', default=r'NLMaps\,v4 Dev Accuracy')
    parser.add_argument('--dataset-to-plot', '-d', default='dev')
    parser.add_argument('--best-accuracy', '-b', type=float)
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
