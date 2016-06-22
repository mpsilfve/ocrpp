#! /usr/bin/env python3

from sys import stdin, argv
from pickle import dump

def add_label(isymbol, osymbol, label_dict):
    if not isymbol in label_dict:
        label_dict[isymbol] = {}
    if not osymbol in label_dict[isymbol]:
        label_dict[isymbol][osymbol] = 0.0
    label_dict[isymbol][osymbol] += 1.0

def normalize(label_dict):
    for isymbol in label_dict:
        tot = sum(label_dict[isymbol].values())
        label_dict[isymbol] = [(count/tot, osym) for (osym, count) in 
                               label_dict[isymbol].items()]
        label_dict[isymbol].sort(reverse=1)

if __name__=='__main__':
    label_dict = {}

    for line in map(lambda x: x.strip(), stdin):
        if line != '':
            isymbol, _sep, osymbol = line.split(' ')
            add_label(isymbol, osymbol, label_dict)
        
    normalize(label_dict)

    out = open(argv[1] + '.lc', 'wb')
    dump(label_dict, out)
