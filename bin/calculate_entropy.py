#!/usr/bin/env python3

import argparse
from collections import defaultdict, deque, Counter
import math


def read_corpus(path):
    with open(path) as f:
        return [line.strip() for line in f]


def tokenize(sentences, order):
    bos_tokens = ['^' * n for n in range(order, 0, -1)]
    eos_token = '$'
    return [
        [*bos_tokens, *sent, eos_token]
        for sent in sentences
    ]


def build_markov_model(sentences, order):
    prefix_counts = Counter()
    conditional_counts = defaultdict(Counter)

    for sent in sentences:
        for i in range(len(sent) - order - 1):
            prefix = tuple(sent[i:i+order])
            token = sent[i+order]
            prefix_counts[prefix] += 1
            conditional_counts[prefix][token] += 1

    return prefix_counts, conditional_counts


def entropy_rate(prefix_counts, conditional_counts):
    return -sum(
        conditional_counts[prefix][token]
        * math.log2(conditional_counts[prefix][token] / prefix_counts[prefix])
        for prefix in prefix_counts
        for token in conditional_counts[prefix]
    ) / sum(prefix_counts.values())


def main(corpus_files, order):
    lines = [line for file in corpus_files for line in read_corpus(file)]
    sentences = tokenize(lines, order)
    prefix_counts, conditional_counts = build_markov_model(sentences, order)
    print(entropy_rate(prefix_counts, conditional_counts))


def parse_args():
    d = 'Calculate the entropy rate of a corpus using a Markov model.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('corpus_files', nargs='+',
                        help='Corpus with one sentence per line.')
    parser.add_argument('--order', '-n', type=int, default=2,
                        help='Order of Markov model. Default: 2 (for trigrams)')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(**vars(ARGS))
