#! /usr/bin/env python3

from sys import stdin

if __name__=='__main__':
    output = 0
    for line in map(lambda x: x.strip(), stdin):
        if line == 'TAGGER OPTIONS':
            output = 0
        if line == 'UNSTRUCTURED FEATURES':
            output = 1

        if output:
            print(line)
