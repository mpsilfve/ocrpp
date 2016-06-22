#! /usr/bin/env python3

from sys import stdin, argv, stderr
from collections import defaultdict
from pickle import dump

def add_pair(i, o, pair_counts):
    if not i in pair_counts:
        pair_counts[i] = {}
    if not o in pair_counts[i]:
        pair_counts[i][o] = 0.0
    pair_counts[i][o] += 1

if __name__=='__main__':
    if len(argv) != 2:
        stderr.write('USAGE: cat data | %s ofile\n' % argv[0])
        exit(1)

    pair_counts = {}

    for line in map(lambda x: x.strip(), stdin):
        if line == '':
            continue
        i, _, o = line.split(' ')
        add_pair(i, o, pair_counts)

    for i, label_counts in pair_counts.items():
        tot = sum(label_counts.values())
        odist = sorted([(c/tot, o) for o, c in label_counts.items()], 
                       reverse=1)
        odist = [(o, m) for m, o in odist]
        pair_counts[i] = odist
            
    dump(pair_counts, open(argv[1], 'wb'))
