# 
# This file is part of SABR.
#
# OpenNetMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenNetMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenNetMon.  If not, see <http://www.gnu.org/licenses/>.

# Special thanks go to Niels van Adrichem and all people connected to the OpenNetmon project, without their work and provided samples OpenNetMon could not have been created in the way it is now.

"""
OpenNetMon.SABR

"""
'''
from pox.lib.revent.revent import EventMixin, Event
from pox.lib.addresses import IPAddr
from pox.lib.packet.vlan import vlan
from pox.lib.packet.ipv4 import ipv4
'''
import os
import sys

from collections import defaultdict
from collections import namedtuple
import requests, json
import urllib
from datetime import datetime
import time
import random
import thread
import uuid
#import threading
#from multiprocessing import Process
from pox.lib.recoco import Timer
import pymongo
from pymongo import MongoClient


from numpy import *
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
from rpy2 import *
import rpy2.robjects as RO
from rpy2.robjects.vectors import IntVector, FloatVector
#from threading import Timer

#log = poxcore.getLogger()
switches = {}
switch_ports = {}


switch_dpid = ["0e-ef-21-f8-fb-44","d6-9a-4f-ab-69-4a", "4a-16-d7-21-a5-4a", "3e-3f-5e-7c-b6-41","2e-23-b1-cc-b9-49","26-49-3e-3d-c9-46","ba-8d-f9-3d-ee-47","d6-dd-ba-d9-3a-4c","1a-01-3c-de-c1-42"]
ct_called = False

s_keys = []
server_list = []

s_keys.append(["s1-c1", "s2-c1", "s3-c1","s4-c1","s5-c1"])
s_keys.append(["s1-c2", "s2-c2", "s3-c2","s4-c2","s5-c2"])
s_keys.append(["s1-c3", "s2-c3", "s3-c3","s4-c3","s5-c3"])
s_keys.append(["s1-c4", "s2-c4", "s3-c4","s4-c4","s5-c4"])


server_list.append("10.10.10.2")
server_list.append("10.10.10.3")
server_list.append("10.10.10.4")
server_list.append("10.10.10.5")
server_list.append("10.10.10.1")
 
clientip_list = []
clientip_list.append("10.10.10.7")
clientip_list.append("10.10.10.8")
clientip_list.append("10.10.10.9")
clientip_list.append("10.10.10.6")



client_port =dict()

client_port["10.10.10.71"]=1
client_port["10.10.10.72"]=1
client_port["10.10.10.73"]=1
client_port["10.10.10.74"]=1
client_port["10.10.10.75"]=1
client_port["10.10.10.81"]=1
client_port["10.10.10.82"]=1
client_port["10.10.10.83"]=1
client_port["10.10.10.84"]=1
client_port["10.10.10.85"]=1
client_port["10.10.10.91"]=5
client_port["10.10.10.92"]=5
client_port["10.10.10.93"]=5
client_port["10.10.10.94"]=5
client_port["10.10.10.95"]=5
client_port["10.10.10.61"]=2
client_port["10.10.10.62"]=2
client_port["10.10.10.63"]=2
client_port["10.10.10.64"]=2
client_port["10.10.10.65"]=2



server_ctrl_ip = []
server_ctrl_ip.append("128.194.6.147")
server_ctrl_ip.append("129.7.98.22")
server_ctrl_ip.append("128.194.6.154")
server_ctrl_ip.append("129.7.98.36")
server_ctrl_ip.append("152.54.14.22")

'''
The following contains the list of IP addresses for all cross traffic generators in the network

'''
cross_list = []
#serv_list.append("10.10.10.5")
cross_list.append("10.10.10.2")
cross_list.append("10.10.10.3")
cross_list.append("10.10.10.5")
cross_list.append("10.10.10.6")
cross_list.append("10.10.10.13")
cross_list.append("10.10.10.14")
cross_list.append("10.10.10.24")
cross_list.append("10.10.10.25")
cross_list.append("10.10.10.26")
cross_list.append("10.10.10.17")
cross_list.append("10.10.10.18")
cross_list.append("10.10.10.28")
cross_list.append("10.10.10.29")
cross_list.append("10.10.10.21")
cross_list.append("10.10.10.22")
cross_list.append("10.10.10.23")
'''
The following is a list of Client IP addresses for the network


'''
client_list = []
#client_list.append("10.10.10.61")    
s_lsps = defaultdict(lambda:defaultdict(lambda:None))
s_ct_lsps1 = []
s_ct_lsps1.append([])
s_ct_lsps1.append([])
s_ct_lsps1.append([])
s_ct_lsps2 = []
s_ct_lsps2.append([])
s_ct_lsps2.append([])
s_ct_lsps2.append([])
s_ct_lsps3 = []
s_ct_lsps3.append([])


arima_ctr=[]
arima_ctr.append(0)
arima_ctr.append(0)
arima_ctr.append(0)
arima_matrix = [[0.0 for x in range(850)] for x in range(3)]
ct_found = []
ct_found.append(0)
ct_found.append(0)
ct_found.append(0)
pos = []
pos.append(0)
pos.append(0)
pos.append(0)

'''
The following contains the information for all paths to the caches from the client
The format is:
(av_bandwidth,no_of_hops,[switch_dpid,out_port,in_port])

Set of clients at switch 3a
'''


s_lsps[s_keys[0][0]]=([0,3,[switch_dpid[3],6,1, switch_dpid[4],2,6,switch_dpid[1],2,5]])
s_lsps[s_keys[0][1]]=([0,3,[switch_dpid[3],4,1, switch_dpid[1],4,1, switch_dpid[2],1,2]])
s_lsps[s_keys[0][2]]=([0,2,[switch_dpid[3],6,1, switch_dpid[4],5,6]])
s_lsps[s_keys[0][3]]=([0,4,[switch_dpid[3],4,1, switch_dpid[1],4,1, switch_dpid[2],5,2,switch_dpid[6],5,3]])
s_lsps[s_keys[0][4]]=([0,3,[switch_dpid[3],4,1, switch_dpid[1],6,1, switch_dpid[0],2,1]])
'''
Set of clients at switch 4a
'''

s_lsps[s_keys[1][0]]=([0,3,[switch_dpid[7],2,1, switch_dpid[3],4,2,switch_dpid[1],2,1]])
s_lsps[s_keys[1][1]]=([0,4,[switch_dpid[7],3,1, switch_dpid[4],2,3, switch_dpid[1],4,5,switch_dpid[2],1,2]])
s_lsps[s_keys[1][2]]=([0,2,[switch_dpid[7],3,1, switch_dpid[4],5,3]])
s_lsps[s_keys[1][3]]=([0,5,[switch_dpid[7],3,1, switch_dpid[4],2,3, switch_dpid[1],4,5,switch_dpid[2],5,2,switch_dpid[6],5,3]])
s_lsps[s_keys[1][4]]=([0,4,[switch_dpid[7],2,1, switch_dpid[3],4,2, switch_dpid[1],6,1,switch_dpid[0],2,1]])


'''
Set of clients at switch 3c
'''
s_lsps[s_keys[2][0]]=([0,3,[switch_dpid[5],4,5, switch_dpid[2],2,7, switch_dpid[1],2,4]])
s_lsps[s_keys[2][1]]=([0,3,[switch_dpid[5],2,5, switch_dpid[6],3,2, switch_dpid[2],1,5]])
s_lsps[s_keys[2][2]]=([0,4,[switch_dpid[5],4,5, switch_dpid[2],2,7, switch_dpid[1],5,4, switch_dpid[4],5,2]])
s_lsps[s_keys[2][3]]=([0,2,[switch_dpid[5],2,5, switch_dpid[6],5,2]])
s_lsps[s_keys[2][4]]=([0,3,[switch_dpid[5],4,5, switch_dpid[2],4,7, switch_dpid[0],2,4]])

'''
Set of clients at switch 4b
'''
s_lsps[s_keys[3][0]]=([0,4,[switch_dpid[8],1,2, switch_dpid[6],3,4,switch_dpid[2],2,5,switch_dpid[1],2,4]])
s_lsps[s_keys[3][1]]=([0,3,[switch_dpid[8],3,2, switch_dpid[5],4,6, switch_dpid[2],1,7]])
s_lsps[s_keys[3][2]]=([0,5,[switch_dpid[8],1,2, switch_dpid[6],3,4, switch_dpid[2],2,5, switch_dpid[1],5,4, switch_dpid[4],5,2]])
s_lsps[s_keys[3][3]]=([0,2,[switch_dpid[8],1,2, switch_dpid[6],5,4]])
s_lsps[s_keys[3][4]]=([0,4,[switch_dpid[8],3,2, switch_dpid[5],4,6, switch_dpid[2],4,7,switch_dpid[0],2,4]])




'''
The following API implements SABR processing, i.e,computes ARIMA forecasts
'''

def _forward_path():
    RO.r('library(forecast)')
    #t = Timer(5.0, _forward_path)
    #t.start()
    print("--------------------FORWARDPATH-------------------")
    start_time=time.time()
    #t = Timer(5, _forward_path)
    #t = Timer(5.0, _forward_path)
    #t.daemon = True
    #t.start()
    #print("ROUTING: Thread_count %d"%threading.activeCount())
    try:
        client=pymongo.MongoClient()
        print( "Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.opencdn
    table = db.portmonitor    
    table1 = db.serv_bandwidth
    #table_list = [db.cache1, db.cache2, db.cache3, db.cache4]
    #cache_ip = ["10.10.10.4","10.10.10.16", "10.10.10.27", "10.10.10.12"]
    best_bw = 100000000000000000.0
    best_serv = 1
    serv_ip = "10.10.10.2"
    hop_count = s_lsps[s_keys[0][0]][1]
    arima_in = []
    #print("TRAFFIC_MATRIX \n")
    for i in range(len(s_keys)):  
      for j in range (len(s_keys[i])):
       print s_keys[i][j]
       min_bw=0.0
       for k in range (3, len(s_lsps[s_keys[i][j]][2])-2,3):
          sum_bw=0.0
          sample_num=0
          arima_in=[]
          #arima_avg=0.0
          quick_avg=0
          for res in table.find({"dpid": str(s_lsps[s_keys[i][j]][2][k]) , "portno": s_lsps[s_keys[i][j]][2][k+2]}).sort([("_id", pymongo.DESCENDING)]).limit(10):
              #print("MONGO: Value of Search Result:\t")
              
              #print(res)
              #stat_query = "{\"dpid\":\"" + str(s_lsps[s_keys[i][j]][2][k]) + "\",\"portno\":"+ str(s_lsps[s_keys[i][j]][2][k+1])+"}"
              #opencdn_url = "http://localhost:27080/opencdn/portmonitor/_find?criteria="+urllib.quote(stat_query)+";batch_size=1"
          
              ##print ("ROUTING PYMONGO URL %s", res)
              #stat_resp = requests.get(res)
              ##print("ROUTING stat_query JSON URL %s", stat_resp)
              #s_resp =stat_resp.json()\
              #print("ROUTING stat_query JSON URL %s", res)
              
              if len(res)>0:
                   quick_avg+=int(res['TXbytes'])
                   if (sample_num%2 == 0):
                       sample_num+=1
                       continue
                   else:
                       arima_in.append(quick_avg/2.0)
                       quick_avg=0
                   sample_num+=1
                   '''
                   if sample_num<=2:
                       sum_bw+=int(res['TXbytes'])
                   #else:
                       #avg_bw=sum_bw/2   
                   avg_bw=sum_bw/2.0
                   '''
          print("ARIMA_API Called\n")
    	  arima_in.reverse()
          arima_in=RO.FloatVector(arima_in)
          #RO.r('library(forecast)')
    	  RO.r('x <- %s'%arima_in.r_repr())
    	  print("ARIMA array loaded\n")
       	  RO.r('fit <- auto.arima(x)')
          print "ARIMA Fit returned\n"
          #RO.r('pdf( "Test%d_%s.pdf" )'%(k,s_keys[i][j]))
          get_res = RO.r('res <- forecast(fit,h=5)')
          sum_arima=0.0
          for arima_iter in range(2,5):
		            sum_arima+=float(robjects.r['res'][3][arima_iter])
          	
          avg_arima=sum_arima/3.0       	  
       	  print("----------ARIMA %f-------------------Port %d--------------IP\t%s\t%s\n"%(avg_arima,s_lsps[s_keys[i][j]][2][k+2], server_list[j], clientip_list[i]))
          #arima_avg=compute_arima(arima_in)
          min_bw=max(avg_arima,min_bw)
          #RO.r('plot(forecast(fit,h=2))')    
          
              
              
          #print("ROUTING MiNBW %d", min_bw)
       '''   
       if best_bw > min_bw:
        best_bw = min_bw
        best_serv=i
       elif best_bw == min_bw:  
        if hop_count>= s_lsps[s_keys[i][j]][1]:
            best_serv=i
            hop_count = s_lsps[s_keys[i][j]][1]
        '''
       s_lsps[s_keys[i][j]][0]= min_bw
       print("----------Final ARIMA %f--------------IP\t%s\t%s\n"%(min_bw, server_list[j], clientip_list[i]))
       post = {"server_ip": server_list[j],"client_ip": clientip_list[i], "min_bw": (min_bw) , "hop_count": hop_count, "date": datetime.utcnow()}
       #post_id = table1.insert_one(post).inserted_id
       if j==len(server_ctrl_ip)-1:
         post_id = table1.insert_one(post).inserted_id
         continue
       post_qual = get_cache_content(server_ctrl_ip[j])
       post.update(post_qual)
       
       '''
       for x, y in post_qual.items():
        print x
        for item in y: # for each item in the list of qualities:
            print item
       '''
       post_id = table1.insert_one(post).inserted_id
      '''
      if s_keys[i][j]=="10.10.10.3": 
        post.update(postq1)
      if s_keys[i][j] == "10.10.10.8":
        post.update(postq2)  
      else:
        post.update(post3)
      '''
      #post.update(gen_random_qual())
      #post_id = table1.insert_one(post).inserted_id
      ##print("Best server is %s and available bandwidth is %d", serv_ip, best_bw)    
      #k=k+1
      #print("ROUTING stat_query WEIGHT %d", min_bw)
      
       #if best_bw > min_bw:
        #   best_bw = min_bw
         #  best_serv = i
         
    end_time = time.time()
    #print("ROUTING: %f", (end_time-start_time))
    #t2 = Timer(5.0, _forward_path)
    ''' 
    if (end_time-start_time) < 5.0:
        time.sleep(5.0-(end_time-start_time))
        #t2 = Timer(5.0, _forward_path)
        #_forward_path
        #t2 = Timer((end_time-start_time), _forward_path) 
    else:
        print("ROUTING: Entered Recursive call-----------------------------------------------------------\n")
        
        #t2 = Timer(5.0, _forward_path)
        #t2.start()
        
        print("ROUTING: Called Timer-----------------------------------------------------------\n")
        
    _forward_path
    '''

def get_cache_content(cache_ip_addr):
    print ("Getting Cached content\n")
    if cache_ip_addr == server_ctrl_ip[len(server_ctrl_ip)-1]:
        return serv_occ
    
    try:
        client=pymongo.MongoClient(cache_ip_addr)
        print( "Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.cachestatus
    table = db.cache1
    cache_occ = defaultdict(list)
    for cache_entry in table.find():
        #print "%s"%str(cache_entry["urn"])
        video_id = str(cache_entry["urn"]).split("/")
        video_id = video_id[0]
        content_id = video_id + "-" + str(cache_entry["seg_no"])
        cache_occ[content_id].append(int(cache_entry["qual_no"]))
    if table.find_one() is not None:
        print cache_ip_addr
        print cache_occ[content_id] 
        #cache_occ[content_id].append(int(cache_entry["qual_no"])+1)
    return cache_occ

def launch():
    global serv_occ
	#poxcore.registerNew(Arima)
    ''' 
    try:
        client=pymongo.MongoClient(server_ctrl_ip[len(server_ctrl_ip)-1])
        print( "Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.cachestatus
    table = db.mpdinfo
    
    for cache_entry in table.find():
        #print "%s"%str(cache_entry["urn"])
        video_id = str(cache_entry["urn"]).split("/")
        video_id = video_id[0]
        content_id = video_id + "-" + str(cache_entry["seg_no"])
        serv_occ[content_id].append(int(cache_entry["quality"]))
    '''
    t = Timer(5.0, _forward_path, recurring=True)	
    '''     
    while True:
    	t = Timer(5.0, _forward_path)
    #threads.append(t)
    	t.start()
        time.sleep(10)
	t.cancel()
	t.join()
    
    #t.start()
    #t.start()
    thread.start_new_thread(create_matrix, ())
    
    t=Timer(5.0, _forward_path, recurring=True)
    t.daemon = True
    t.start()
    
    #_forward_path
    
    while True: 
    	p = Process(target=_forward_path)
    	p.start()
    	time.sleep(5)
	'''
    #p.join()
      
#if __name__ == "__main__":
 #   sys.exit(main()) 

