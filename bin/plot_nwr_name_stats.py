#!/usr/bin/env python3

import argparse

import matplotlib
matplotlib.use('pgf')
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": ["Linux Libertine O"],
    "font.sans-serif": ["Linux Libertine O"],
}
matplotlib.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pyplot as plt


def main(stats_tsv, outfile, title=None):
    area_to_count = {}
    with open(stats_tsv) as f:
        for line in f:
            area, count = line.strip().split('\t')
            area_to_count[area] = int(count)

    areas, counts = zip(*sorted(area_to_count.items(),
                                key=lambda item: item[1], reverse=True))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(counts)), counts, 'bo', markersize=4)
    ax.set_xlabel('Names ({} in total)'.format(len(areas)))
    ax.set_ylabel('Name Usage Count')
    if title:
        ax.set_title(title)

    fig.tight_layout()

    fig.savefig(outfile)

    return fig


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('stats_tsv')
    parser.add_argument('outfile')
    parser.add_argument('--title', '-t')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
