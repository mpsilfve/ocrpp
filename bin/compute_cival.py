#! /usr/bin/env python3

from sys import stdin

import numpy as np
import scipy as sp
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return 100*m, 100*h

data = [float(d) for d in stdin.read().split('\n') if d != '']
print ("%.2f +/- %.2f" %  mean_confidence_interval(data))
