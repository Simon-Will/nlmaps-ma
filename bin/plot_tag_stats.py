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


def load_stats(stats_tsv):
    tag_to_count = {}
    with open(stats_tsv) as f:
        for line in f:
            tag, count = line.strip().split('\t')
            tag_to_count[tag] = int(count)

    tags, counts = zip(*sorted(tag_to_count.items(),
                               key=lambda item: item[1], reverse=True))
    return tags, counts


def main(stats_tsvs, labels=None, outfile=None, log_scale=False, title=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if labels:
        labels = labels.split('|')
        print(labels)
    else:
        labels = [None] * len(stats_tsvs)

    for stats_tsv, label in zip(stats_tsvs, labels):
        tags, counts = load_stats(stats_tsv)
        ax.plot(range(len(counts)), counts, 'o', markersize=3, label=label)
        if len(stats_tsvs) == 1:
            ax.set_xlabel('Tags ({} in total)'.format(len(tags)))
        else:
            ax.set_xlabel('Tag Index')
        ax.set_ylabel('Tag Usage Count')

    if log_scale:
        ax.set_yscale('log')
    if title:
        ax.set_title(title)
    if labels:
        ax.legend()
    fig.tight_layout()

    if outfile:
        fig.savefig(outfile)

    return fig


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('stats_tsvs', nargs='+')
    parser.add_argument('--outfile', '-o', default='counts.png')
    parser.add_argument('--log-scale', action='store_true', default=True)
    parser.add_argument('--title', '-t')
    parser.add_argument('--labels', '-l')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
