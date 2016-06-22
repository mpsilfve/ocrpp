#! /usr/bin/env python3

from sys import argv, stderr

sys_file = open(argv[1])
gold_file = open(argv[2])

tot = 0.0
corr = 0.0

for sys_out, gold_line in zip(map(lambda x: x.strip(), sys_file),
                              map(lambda x: x.strip(), gold_file)):
    gold_in, gold_out = gold_line.split(' ')
    if sys_out == gold_out:
        corr += 1
    tot += 1

print ("word accuracy rate: %.4f" % (corr/tot))
