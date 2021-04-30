#!/usr/bin/env python3

import argparse
import json

import matplotlib
matplotlib.use('pgf')
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": ["Linux Libertine O"],
    "font.sans-serif": ["Linux Libertine O"],
}
matplotlib.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pyplot as plt


def main(errors_json, outfile):
    errors = json.load(open(errors_json))
    error_classes = list(reversed(errors[0].keys()))
    error_class_counts = [
        sum(errs[error_class] for errs in errors)
        for error_class in error_classes
    ]
    other_index = (error_classes.index('other')
                   if 'other' in error_classes else None)
    if other_index is not None and error_class_counts[other_index] == 0:
        error_classes.pop(other_index)
        error_class_counts.pop(other_index)

    total = len(errors)
    error_class_percentages = [
        count / total
        for count in error_class_counts
    ]
    percentages_left = [1 - perc for perc in error_class_percentages]
    print(error_classes)
    print(error_class_counts)

    fig = plt.figure(figsize=(6.4, 3.5))
    ax = fig.add_subplot(111)

    #ind = [i / 2 for i in range(len(error_class_percentages))]
    ind = range(len(error_class_percentages))
    width = 0.5
    plt_false, *_ = ax.barh(ind, error_class_percentages, width, color='red')
    pale_green = '#c1fcc1'
    ax.barh(ind, percentages_left, width, left=error_class_percentages,
            color=pale_green)

    #ax.set_title('Percentage of Parses with Specific Errors')
    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel('Percentage')
    ax.set_yticks(ind)
    ax.set_xlim(0.0, 1.0)
    ax.set_yticklabels(error_classes, fontsize=12)
    fig.subplots_adjust(left=0.16, bottom=0.14, right=0.98, top=0.98)

    fig.savefig(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('errors_json')
    parser.add_argument('outfile')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
