#! /usr/bin/env python3

from sys import stdin, argv, stderr
from libhfst import HfstInputStream

def select(predictions, dictionary, top_n = -1):
    for i, pred in enumerate(predictions):
        if top_n > 0 and i >= top_n:
            break
        if len(dictionary.lookup(pred)) > 0:
            return pred

    return predictions[0]

if __name__=='__main__':
    if len(argv) != 3:
        stderr.write("USAGE: cat predictions | %s dict.hfst top_n" % argv[0])

    dictionary = HfstInputStream(argv[1]).read()
    top_n = int(argv[2])

    predictions = []

    for line in map(lambda x: x.strip(), stdin):
        if line == '':
            if predictions != []:
                print(select(predictions, dictionary, top_n))
            predictions = []
        else:
            predictions.append(line)

    if predictions != []:
        print(select(predictions))
