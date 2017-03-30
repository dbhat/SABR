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
STARTUP_qual=150
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

def spectrum_calc(bitrate_history):


	bitrates = [89283.0, 262537.0, 791182.0, 2484135.0, 4219897.0]
	q_layer = []
	br_qlayer = {}


	for i in bitrates:
		q = i / 89283.0
		q_layer.append(q)
		br_qlayer.update({i:q})
	#print q_layer
	#print br_qlayer

	zh = 0
	zt = 0
	second_half_total = 0
	second_half = 0.0
	num_change = 0
	for j in range(1, len(bitrate_history)):
		if bitrate_history[j] != bitrate_history[j-1]:
			for i in range(1, len(bitrate_history)):
				if bitrate_history[i] != bitrate_history[i-1]:
					zh = zh + abs(bitrates.index(bitrate_history[i]) - bitrates.index(bitrate_history[i-1]))
					#print bitrates.index(bitrate_history[i])
					#print bitrates.index(bitrate_history[i-1])
					#print zh
					num_change = num_change + 1
				#num_change = zh
			#print num_change
			#print "zh " + str(zh)
			zzh = (1 / float(num_change)) * float(zh)
			#print zzh
		
			ht = bitrates.index(bitrate_history[j])
			#print ht
			second_half = (ht - zzh) ** 2
		#    print second_half
			if bitrate_history[j] != bitrate_history[j-1]:
				zt = zt + second_half
				#print zt
	return zt



first_file_name =[]
first_file_name.append(init_file_name)
index=0
file_index=0
last_start_arr = []
end_time_arr = []
all_start_time = []
check_dash = []
check_dash2 = []

sara_unfin=0
rebuf_arr = []
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_bolao_v*/bola//dash_buffer*/DASH_BUFFER*'):
	list_quals=np.genfromtxt(name,delimiter=',', usecols=1, dtype=float)
	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)
	#list_time=list_time-list_time[1]

	list_quals=list_quals[~np.isnan(list_quals)]
	
	if list_quals.size>5:
		rebuffering_perc = (list_time[len(list_time)-1] - 299.0)*100/ 299.0
		if (list_time[len(list_time)-1] - 299.0)<0:
			print name
			sara_unfin+=1
		else:
			rebuf_arr.append(rebuffering_perc)

print "BOLAO_qual"
print "Rebuffering Time"
sabr_unfin=0
nparry2 = np.asarray(rebuf_arr)
avg_avgbr2=nparry2.mean()
sd_avgbr2=np.std(nparry2)
print avg_avgbr2
print sd_avgbr2
print sara_unfin
rebuf_arr2 = []
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_quality_lru_bolao_v*/sabr_bola/dash_buffer*/DASH_BUFFER_*'):
	list_quals=np.genfromtxt(name,delimiter=',', usecols=1, dtype=float)
	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)

	list_quals=list_quals[~np.isnan(list_quals)]
	
	if list_quals.size>5:
		rebuffering_perc = (list_time[len(list_time)-1] - 299.0)*100/ 299.0
		if (list_time[len(list_time)-1] - 299.0)<0:
			print name
			sabr_unfin+=1
		else:
			rebuf_arr2.append(rebuffering_perc)

print "SABR - BOLAO_qual"
print "Rebuffering Time"
nparry = np.asarray(rebuf_arr2)
avg_avgbr=nparry.mean()
sd_avgbr=np.std(nparry)
print avg_avgbr
print sd_avgbr
print sabr_unfin
with open('abr_rebuffers_BOLAO_qual.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(rebuf_arr, rebuf_arr2))

print "Magnitude and Quality"
print "BOLAO_qual"
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_bolao_v*/bola//server_log*/SERVER*'):
	f1=open(name)
	lines = f1.readlines()[1:]
	if len(lines)>5:
		prev_row = None
		cnt=0
		sum=0.0
		mag_switches =0.0
		for line in lines:
			row1 = line.split(",")
			sum+=float(row1[2])
			if prev_row != None :
				if (prev_row[2] != row1[2]):
					cnt+=1
					mag_switches += math.fabs((float(prev_row[2]) - float(row1[2])))
			prev_row = row1
		cnt_of_switches.append(cnt)
		mag_of_switches.append((mag_switches/1000000)/cnt)
		f1.close()

cnt_of_switches = np.asarray(cnt_of_switches)
mag_of_switches = np.array(mag_of_switches)


avg_cntsw=cnt_of_switches.mean()
sd_cntsw=np.std(cnt_of_switches)
print avg_cntsw
print sd_cntsw

avg_magsw=mag_of_switches.mean()
sd_magsw=np.std(mag_of_switches)
print avg_magsw
print sd_magsw



print "SABR - BOLAO_qual"

for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_quality_lru_bolao_v*/sabr_bola/server_log*/SERVER*'):
	
	f1=open(name)
	lines = f1.readlines()[1:]
	if len(lines)>5:
		prev_row = None
		cnt=0
		sum=0.0
		mag_switches2 =0.0
		for line in lines:
			row1 = line.split(",")
			sum+=float(row1[2])
			if prev_row != None :
				if (prev_row[2] != row1[2]):
					cnt+=1
					mag_switches2+= math.fabs((float(prev_row[2]) - float(row1[2])))
			prev_row = row1
		cnt_of_switches2.append(cnt)
		mag_of_switches2.append((mag_switches2/1000000/cnt))
		f1.close()


cnt_of_switches2 = np.asarray(cnt_of_switches2)
mag_of_switches2 = np.array(mag_of_switches2)


avg_cntsw2=cnt_of_switches2.mean()
sd_cntsw2=np.std(cnt_of_switches2)
print avg_cntsw2
print sd_cntsw2

avg_magsw2=mag_of_switches2.mean()
sd_magsw2=np.std(mag_of_switches2)
print avg_magsw2
print sd_magsw2
with open('abr_numofswitches_BOLAO_qual.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(cnt_of_switches, cnt_of_switches2))
    


count=0
spectrum_array = []
print "Bitrates"
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_bolao_v*/bola//server_log*/SERVER_LOG*'):
	count+=1
	list_quals=np.genfromtxt(name,delimiter=',', usecols=2, dtype=float)
	list_time=np.genfromtxt(name,delimiter=',', usecols=0, dtype=float)
	spectrum_array.append(spectrum_calc(list_quals[1:]))
	if list_quals.size>5:
		x = list_quals[~np.isnan(list_quals)].mean()
		bitrate_array.append(x/1000000.0)
nparry = np.asarray(bitrate_array)

avg_avgbr=nparry.mean()
sd_avgbr=np.std(nparry)
print "BOLAO_qual"
print avg_avgbr
print sd_avgbr
print "Spectrum"
nparry = np.asarray(spectrum_array)
avg_avgbr=nparry.mean()
sd_avgbr=np.std(nparry)
print "BOLAO_qual"
print avg_avgbr
print sd_avgbr

print "COUNT"
print count
count=0
spectrum_array2 = []
for name in glob.glob('/Users/dbhat/Documents/opencdn/ACM_MM/CloudLab/10runs_quality_lru_bolao_v*/sabr_bola/server_log*/SERVER*'):
	count+=1
	list_quals=np.genfromtxt(name,delimiter=',', usecols=2, dtype=float)
	spec_qual = spectrum_calc(list_quals[1:])
	spectrum_array2.append(spec_qual)
	if list_quals.size>5:
		x = list_quals[~np.isnan(list_quals)].mean()
		bitrate_array2.append(x/1000000.0)

nparry2 = np.asarray(bitrate_array2)
avg_avgbr2=nparry2.mean()
sd_avgbr2=np.std(nparry2)
print "SABR - BOLAO_qual"
print avg_avgbr2
print sd_avgbr2
print "Spectrum"
nparry2 = np.asarray(spectrum_array2)
avg_avgbr2=nparry2.mean()
sd_avgbr2=np.std(nparry2)
print "SABR - BOLAO_qual"
print avg_avgbr2
print sd_avgbr2



with open('abr_fullcap_rate_BOLAO_qual.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(bitrate_array, bitrate_array2))
	#writer.write
with open('abr_magofswitches_BOLAO_qual.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(spectrum_array, spectrum_array2))


