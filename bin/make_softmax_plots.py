#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def plot_softmax(a, filename):
    sm = softmax(a)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    bars = ax.bar(range(len(a)), sm)

    for bar in bars:
        y = bar.get_height()
        plt.text(bar.get_x(), y + 0.05, '{:.3f}'.format(y))

    ax.set_xlim(-1, 10)
    ax.set_ylim(0, 1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xticks(range(10))

    fig.savefig(filename)


def main():
    a = np.random.randn(10)
    a[4] = 1.5
    a[6] = 3.0
    plot_softmax(a, 'softmax1.png')
    a[:4] = - np.inf
    a[5] = - np.inf
    a[7:] = -np.inf
    plot_softmax(a, 'softmax2.png')


if __name__ == '__main__':
    main()
