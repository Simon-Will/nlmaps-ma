#!/usr/bin/env python3

from collections import defaultdict, namedtuple
import os
import sys

import matplotlib.pyplot as plt


Record = namedtuple('Record', ('model', 'dataset', 'step', 'score'))


def read_records(infile):
    records = defaultdict(list)
    with open(infile) as f:
        for line in f:
            model, dataset, step, correct, total = line.strip().split('|')
            score = int(correct) / int(total)
            records[(model, dataset)].append(
                Record(model, dataset, int(step), score)
            )
    return records


def plot_curve(ax, steps, accuracies, **kwargs):
    ax.plot(steps, accuracies, **kwargs)


def main():
    infile = sys.argv[1]
    dataset_to_plot = sys.argv[2] if len(sys.argv) > 2 else 'dev'
    outfile = sys.argv[3] if len(sys.argv) > 3 else 'out.png'

    records_by_model = read_records(infile)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for (model, dataset), records in records_by_model.items():
        if dataset == dataset_to_plot:
            steps = [r.step for r in records]
            scores = [r.score for r in records]
            plot_curve(ax, steps, scores, label=model)

    ax.legend()
    #ax.set_xlim(0, 200)
    #ax.set_ylim(0.55, 0.7)
    ax.set_xlabel('Steps')
    ax.set_ylabel('NLMaps v3 Dev Accuracy')

    #OUT_DIR = '/home/gorgor/ma/nlmaps-ma/plots'
    #outfile = os.path.join(OUT_DIR, 'online-learning-curve.png')
    fig.savefig(outfile)


if __name__ == '__main__':
    main()
