#! /usr/bin/env python3

from sys import stdin, stdout

def select(predictions):
    return predictions[0]

if __name__=='__main__':
    predictions = []

    for line in map(lambda x: x.strip(), stdin):
        if line == '':
            if predictions != []:
                print(select(predictions))
                stdout.flush()
            predictions = []
        else:
            predictions.append(line)

    if predictions != []:
        print(select(predictions))
