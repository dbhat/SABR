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
STARTUP_QUAL=150
bitrate_array =[]
time_to_completion = []
cnt_of_switches = []
mag_of_switches = []
bitrate_array2 =[]
time_to_completion2 = []
cnt_of_switches2 = []
mag_of_switches2 = []
num_of_rebuffers = []
num_of_rebuffers2 = []
bitrate_array3 =[]
time_to_completion3 = []
cnt_of_switches3 = []
mag_of_switches3 = []
num_of_rebuffers3 = []
VIDEO_DURATION=300.0

bitrates = [89283.0, 262537.0, 791182.0, 2484135.0, 4219897.0]
cache_list=["10.10.10.4","10.10.10.16","10.10.10.12","10.10.10.27"]
count=0
spectrum_array = []


c_q1=0.0
c_q2=0.0
c_q3=0.0
c_q4=0.0
c_q5=0.0
q1=0
q2=0
q3=0
q4=0
q5=0
sum_q1=0
sum_q2=0
sum_q3=0
sum_q4=0
sum_q5=0
bola_qual1=[]
bola_qual2=[]
bola_qual3=[]
bola_qual4=[]
bola_qual5=[]
num_bola_qual1=[]
num_bola_qual2=[]
num_bola_qual3=[]
num_bola_qual4=[]
num_bola_qual5=[]

print "Bitrates"
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_quality_lru_bolao_v*/sabr_bola/server_log*/SERVER_LOG*'):
	
	count+=1
	list_quals=np.genfromtxt(name,delimiter=',', usecols=2, dtype=float)

	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)
	list_serv=np.genfromtxt(name,delimiter=',', usecols=1, dtype="|S11")
	if len(list_serv)<151:
		print name
	list_quals=list_quals[~np.isnan(list_quals)]
	sum_q1+=(c_q1+q1)
	sum_q2+=(c_q2+q2)
	sum_q3+=(c_q3+q3)
	sum_q4+=(c_q4+q4)
	sum_q5+=(c_q4+q5)
	
	if count%60==0:
		if q1+c_q1>0:
			bola_qual1.append(c_q1/(q1+c_q1))
		elif q1+c_q1==0:
			bola_qual1.append(0)
		if q2+c_q2>0:
			bola_qual2.append(c_q2/(q2+c_q2))
		elif q2+c_q2==0:
			bola_qual2.append(0)
		if q3+c_q3>0:
			bola_qual3.append(c_q3/(q3+c_q3))
		elif q3+c_q3==0:
			bola_qual3.append(0)
		if q4+c_q4>0:
			bola_qual4.append(c_q4/(q4+c_q4))
		elif q4+c_q4==0:
			bola_qual4.append(0)
		if q5+c_q5>0:
			bola_qual5.append(c_q5/(q5+c_q5))
		elif q5+c_q5==0:
			bola_qual5.append(0)
		c_q1=0.0
		c_q2=0.0
		c_q3=0.0
		c_q4=0.0
		c_q5=0.0
		q1=0
		q2=0
		q3=0
		q4=0
		q5=0
	
	for item,item2 in zip(list_quals,list_serv):
		if item == bitrates[0]:
			if item2 in cache_list:
				c_q1+=1
			else:
				q1+=1
		if item == bitrates[1]:
			if item2 in cache_list:
				c_q2+=1
			else:
				q2+=1
		if item == bitrates[2]:
			if item2 in cache_list:
				c_q3+=1
			else:
				q3+=1
		if item == bitrates[3]:
			if item2 in cache_list:
				c_q4+=1
			else:
				q4+=1
		if item == bitrates[4]:
			if item2 in cache_list:
				c_q5+=1
			else:
				q5+=1



print count

with open('qual_hitratio_BOLA_glob_qual.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(bola_qual1,bola_qual2,bola_qual3,bola_qual4,bola_qual5))
	#writer.write

