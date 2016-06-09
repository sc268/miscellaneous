import numpy as np
import pandas as pd
import scipy as sp
import os 


import os

os.chdir('/Users/schang/Dropbox/codes/2015_TIBA/code/python')
print os.getcwd()

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import os 


import json

os.chdir('/Users/schang/Dropbox/codes/2015_TIBA/code/python')
print os.getcwd()


def read_dat(path):
    return pd.read_csv(path , skiprows=1, sep=';', header = None, \
                       names = ['t', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz'])


true1 = read_dat("../../data/exercise1_data/true1_1.csv")
true2 = read_dat("../../data/exercise1_data/true1_2.csv")
true3 = read_dat("../../data/exercise1_data/true1_3.csv")

false1 = read_dat("../../data/exercise1_data/false1_1.csv")
false2 = read_dat("../../data/exercise1_data/false1_2.csv")

print true1.columns


# PWD 2nd approach
from scipy.interpolate import interp1d
from scipy.signal import periodogram


def total_dist(dat1, dat2):
    sensors = (dat1.columns).drop('t')
    total = 0 
    for sensor in sensors:

        freq1, psd1 = periodogram(dat1[sensor], 30)
        plt.semilogy(freq1, psd1)

        freq2, psd2 = periodogram(dat2[sensor], 30)
        plt.semilogy(freq2, psd2)

        #compute distance
        init = max(freq1[0], freq2[0])#max(min(freq1), min(freq2))
        end = min(freq1[-1], freq2[-1])#min(max(freq1), max(freq2))

        freq_overlapped = np.arange( init, end, (end-init)/300)
        fit1 = interp1d(freq1, psd1)
        fit2 = interp1d(freq2, psd2)

        #fit:
        dd = 10
        dist = np.mean(( np.convolve(fit1(freq_overlapped), np.ones(dd)/dd) -\
                         np.convolve(fit2(freq_overlapped), np.ones(dd)/dd))**2)
        total += dist
    print "%.3f" % total


total_dist(true1, true2)
total_dist(true1, true3)
total_dist(true2, true3)
print 
total_dist(true1, false1)
total_dist(true1, false2)
total_dist(true2, false1)
total_dist(true2, false2)



