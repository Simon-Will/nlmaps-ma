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


def get_color(class_):
    if class_ == 'correct':
        # green
        return (44/256, 160/256, 44/256)
    if class_ == 'tag_present':
        # blue
        return (31/256, 119/256, 180/256)
    # red
    return (214/256, 39/256, 40/256)


def get_marker(class_):
    if class_ == 'correct':
        return 'x'
    if class_ == 'tag_present':
        return 'o'
    return '^'



def main(online_analysis, outfile):
    with open(online_analysis, 'r') as f:
        analysis = json.load(f)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    tags, results = zip(*sorted(analysis.items(), key=lambda kv: kv[0],
                                reverse=True))

    ind = range(1, len(tags) + 1)
    for i, (_, result) in enumerate(zip(tags, results), 1):
        for step, class_ in result:
            ax.plot([step], [i], color=get_color(class_), marker=get_marker(class_))

    xmin, xmax = -30, 2400
    ax.hlines(ind, xmin, xmax, colors='lightgray')

    ax.set_xlim(xmin, xmax)
    ax.set_xlabel('Instance')
    ax.set_yticks(ind)
    ax.set_yticklabels(tags)

    fig.tight_layout()

    fig.savefig(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('online_analysis')
    parser.add_argument('outfile')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
