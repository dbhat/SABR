#!/bin/python

import datetime
import numpy as np
import pandas as pd
from itertools import cycle
from matplotlib import pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
import datetime as dt
import time
import dateutil
from StringIO import StringIO
import math
import glob
from pylab import *
import csv
from itertools import izip
import statsmodels.api as sm # recommended import according to the docs
VIDEO_DURATION=300.0

bitrates = [89283.0, 262537.0, 791182.0, 2484135.0, 4219897.0]

count=0
spectrum_array = []


q1=0
q2=0
q3=0
q4=0
q5=0
print "Bitrates"
for name in glob.glob('<Path_to_results>/10runs_quality_lru_bolao_v*/sabr_bola/server_log*/SERVER_LOG*'):

	count+=1
	list_quals=np.genfromtxt(name,delimiter=',', usecols=2, dtype=float)
	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)
	list_quals=list_quals[~np.isnan(list_quals)]
	for item in list_quals:
		if item == bitrates[0]:
				q1+=1
		if item == bitrates[1]:
				q2+=1
		if item == bitrates[2]:
				q3+=1
		if item == bitrates[3]:
				q4+=1
		if item == bitrates[4]:
				q5+=1

s_q1=0
s_q2=0
s_q3=0
s_q4=0
s_q5=0
print "BOLA"
print count
bola_qual=[]
bola_qual.append(q1)
bola_qual.append(q2)
bola_qual.append(q3)
bola_qual.append(q4)
bola_qual.append(q5)

nparry2 = np.asarray(bola_qual)
avg_avgbr2=nparry2.mean()
sd_avgbr2=np.std(nparry2)

print sd_avgbr2

count=0

for name in glob.glob('<Path_to_results>/10runs_quality_lru_squad_v*/sabr_squad/server_log*/SERVER*'):
	count+=1
	list_quals=np.genfromtxt(name,delimiter=',', usecols=3, dtype=float)
	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)
	list_quals=list_quals[~np.isnan(list_quals)]
	for item in list_quals:
		if item == bitrates[0]:
				s_q1+=1
		if item == bitrates[1]:
				s_q2+=1
		if item == bitrates[2]:
				s_q3+=1
		if item == bitrates[3]:
				s_q4+=1
		if item == bitrates[4]:
				s_q5+=1
print "SQUAD"
print count
squad_qual=[]
squad_qual.append(s_q1)
squad_qual.append(s_q2)
squad_qual.append(s_q3)
squad_qual.append(s_q4)
squad_qual.append(s_q5)
nparry2 = np.asarray(squad_qual)

avg_avgbr2=nparry2.mean()
sd_avgbr2=np.std(nparry2)

print sd_avgbr2

with open('qual_dist_BOLA_SQUAD.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(bola_qual, squad_qual))



