# #Copyright (C) 2013, Delft University of Technology, Faculty of Electrical Engineering, Mathematics and Computer Science, Network Architectures and Services, Niels van Adrichem
#
# This file is part of OpenNetMon.
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
from operator import pos

# Special thanks go to James McCauley and all people connected to the POX project, without their work and provided samples OpenNetMon could not have been created in the way it is now.

"""
OpenNetMon.Forwarding

Requires openflow.discovery
"""

from pox.lib.revent.revent import EventMixin, Event
from pox.lib.addresses import IPAddr
from pox.lib.packet.vlan import vlan
from pox.lib.packet.ipv4 import ipv4
from pox.lib.recoco import Timer



import pox.lib.util as poxutil
from pox.core import core as poxcore

import pox.openflow.libopenflow_01 as of
from collections import defaultdict
import pox.lib.packet as pkt

from collections import namedtuple
import requests, json
import urllib
from datetime import datetime
import time
import random

#import threading
#from multiprocessing import Process

import pymongo
from pymongo import MongoClient

log = poxcore.getLogger()

switches = {}
switch_ports = {}
'''
The following contains the list of DPIDs for all switches in the network

'''
switch_dpid = ["22-77-89-c9-39-46","3a-7a-27-30-9e-46", "8a-4b-6a-50-24-49", "c6-08-4b-80-02-43","06-93-3b-c4-95-42","16-93-0c-f4-b7-4e","7e-50-18-13-f8-4b","56-23-ff-96-21-4c","72-82-05-4f-87-42"]
ct_called = False

s_keys = []
server_list = []

s_keys.append(["s1-c1", "s2-c1", "s3-c1","s4-c1","s5-c1"])
s_keys.append(["s1-c2", "s2-c2", "s3-c2","s4-c2","s5-c2"])
s_keys.append(["s1-c3", "s2-c3", "s3-c3","s4-c3","s5-c3"])
s_keys.append(["s1-c4", "s2-c4", "s3-c4","s4-c4","s5-c4"])


server_list.append("10.10.10.4")
server_list.append("10.10.10.12")
server_list.append("10.10.10.16")
server_list.append("10.10.10.27")
server_list.append("10.10.10.1")
 
clientip_list = []
clientip_list.append("10.10.10.7")
clientip_list.append("10.10.10.6")
clientip_list.append("10.10.10.8")
clientip_list.append("10.10.10.9")



client_port =dict()

client_port["10.10.10.71"]=11
client_port["10.10.10.72"]=10
client_port["10.10.10.73"]=2
client_port["10.10.10.74"]=1
client_port["10.10.10.75"]=4
client_port["10.10.10.61"]=6
client_port["10.10.10.62"]=5
client_port["10.10.10.63"]=4
client_port["10.10.10.64"]=3
client_port["10.10.10.65"]=2
client_port["10.10.10.81"]=10
client_port["10.10.10.82"]=9
client_port["10.10.10.83"]=8
client_port["10.10.10.84"]=7
client_port["10.10.10.85"]=6
client_port["10.10.10.91"]=3
client_port["10.10.10.92"]=4
client_port["10.10.10.93"]=5
client_port["10.10.10.94"]=7
client_port["10.10.10.95"]=6


'''
The following contains the list of IP addresses for all cross traffic generators in the network

'''
cross_list = []
#serv_list.append("10.10.10.5")

cross_list.append("10.10.10.1")
cross_list.append("10.10.10.3")
cross_list.append("10.10.10.22")
cross_list.append("10.10.10.23")
cross_list.append("10.10.10.30")
cross_list.append("10.10.10.39")
cross_list.append("10.10.10.24")
cross_list.append("10.10.10.120")
cross_list.append("10.10.10.100")
cross_list.append("10.10.10.10")
cross_list.append("10.10.10.6")
cross_list.append("10.10.10.7")
cross_list.append("10.10.10.8")
cross_list.append("10.10.10.9")


'''
The following is a list of Client IP addresses for the network


'''
client_list = []
#client_list.append("10.10.10.61")    
s_lsps = defaultdict(lambda:defaultdict(lambda:None))


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


s_lsps[s_keys[0][0]]=([0,3,[switch_dpid[3],3,0, switch_dpid[1],6,3]])
s_lsps[s_keys[0][1]]=([0,3,[switch_dpid[3],5,0, switch_dpid[1],2,3, switch_dpid[2],7,3]])
s_lsps[s_keys[0][2]]=([0,2,[switch_dpid[3],3,0, switch_dpid[4],6,1]])
s_lsps[s_keys[0][3]]=([0,4,[switch_dpid[3],5,0, switch_dpid[1],2,3, switch_dpid[2],1,3,switch_dpid[6],2,1]])
s_lsps[s_keys[0][4]]=([0,3,[switch_dpid[3],5,0, switch_dpid[1],1,3, switch_dpid[0],3,4]])
'''
Set of clients at switch 4a
'''

s_lsps[s_keys[1][0]]=([0,3,[switch_dpid[7],7,0, switch_dpid[3],5,9,switch_dpid[1],6,3]])
s_lsps[s_keys[1][1]]=([0,4,[switch_dpid[7],1,0, switch_dpid[4],3,2, switch_dpid[1],2,4,switch_dpid[2],7,3]])
s_lsps[s_keys[1][2]]=([0,2,[switch_dpid[7],1,0, switch_dpid[4],6,2]])
s_lsps[s_keys[1][3]]=([0,5,[switch_dpid[7],1,0, switch_dpid[4],3,2, switch_dpid[1],2,4,switch_dpid[2],1,3,switch_dpid[6],2,1]])
s_lsps[s_keys[1][4]]=([0,4,[switch_dpid[7],7,0, switch_dpid[3],5,9, switch_dpid[1],1,3,switch_dpid[0],3,4]])


'''
Set of clients at switch 3c
'''
s_lsps[s_keys[2][0]]=([0,3,[switch_dpid[5],4,0, switch_dpid[2],3,4, switch_dpid[1],6,2]])
s_lsps[s_keys[2][1]]=([0,3,[switch_dpid[5],4,0, switch_dpid[2],7,4]])
s_lsps[s_keys[2][2]]=([0,4,[switch_dpid[5],4,0, switch_dpid[2],3,4, switch_dpid[1],4,2, switch_dpid[4],6,3]])
s_lsps[s_keys[2][3]]=([0,2,[switch_dpid[5],3,0, switch_dpid[6],2,3]])
s_lsps[s_keys[2][4]]=([0,3,[switch_dpid[5],4,0, switch_dpid[2],2,4, switch_dpid[0],3,5]])

'''
Set of clients at switch 4b
'''
s_lsps[s_keys[3][0]]=([0,4,[switch_dpid[8],1,0, switch_dpid[6],1,4,switch_dpid[2],3,1,switch_dpid[1],6,2]])
s_lsps[s_keys[3][1]]=([0,3,[switch_dpid[8],2,0, switch_dpid[5],4,5, switch_dpid[2],7,4]])
s_lsps[s_keys[3][2]]=([0,5,[switch_dpid[8],1,0, switch_dpid[6],1,4, switch_dpid[2],3,1, switch_dpid[1],4,2, switch_dpid[4],6,3]])
s_lsps[s_keys[3][3]]=([0,2,[switch_dpid[8],1,0, switch_dpid[6],2,4]])
s_lsps[s_keys[3][4]]=([0,4,[switch_dpid[8],2,0, switch_dpid[5],4,5, switch_dpid[2],2,4,switch_dpid[0],3,5]])


'''
The following contains the information for all cross traffic paths in the network
The format is:
(av_bandwidth,no_of_hops,[switch_dpid,out_port,in_port])
client,server
'''

s_ct_lsps = {}
s_ct_lsps[("10.10.10.1","10.10.10.23")] = [switch_dpid[0],3,5, switch_dpid[1],7,1]
s_ct_lsps[("10.10.10.3","10.10.10.39")] = [switch_dpid[0],1,2, switch_dpid[2],3,6]
s_ct_lsps[("10.10.10.22","10.10.10.39")] = [switch_dpid[1],3,5, switch_dpid[2],3,1]
s_ct_lsps[("10.10.10.30","10.10.10.23")] = [switch_dpid[2],1,4, switch_dpid[1],7,3]
s_ct_lsps[("10.10.10.23","10.10.10.24")] = [switch_dpid[1], 6,7, switch_dpid[3],5,6]
s_ct_lsps[("10.10.10.39","10.10.10.100")] = [switch_dpid[2], 7,3, switch_dpid[5],4,6]
s_ct_lsps[("10.10.10.22","10.10.10.6")] = [switch_dpid[1], 4,5, switch_dpid[4],6,3]
s_ct_lsps[("10.10.10.30","10.10.10.9")] = [switch_dpid[2], 5,4, switch_dpid[6],3,6]

'''
s_ct_lsps[("10.10.10.5","10.10.10.25")] = [switch_dpid[1], 5,3, switch_dpid[3],6,9]
s_ct_lsps[("10.10.10.13","10.10.10.22")] = [switch_dpid[2], 5,2, switch_dpid[6],2,9]
s_ct_lsps[("10.10.10.4","10.10.10.17")] = [switch_dpid[1], 4,2, switch_dpid[4],1,4]
s_ct_lsps[("10.10.10.12","10.10.10.28")] = [switch_dpid[2], 4,1, switch_dpid[5],2,1]

s_ct_lsps2 [0].extend([switch_dpid[0],4,3, switch_dpid[1],3,6])
s_ct_lsps2 [0].extend([switch_dpid[0], 5,1, switch_dpid[2],2,6])
s_ct_lsps3 [0].extend([switch_dpid[6], 4,1, switch_dpid[2],3,4,switch_dpid[5],3,4])

s_ct_lsps2 [0].extend([switch_dpid[0], 1,2, switch_dpid[3],2,3, switch_dpid[2],1,3])
s_ct_lsps2 [1].extend([switch_dpid[0], 5,2, switch_dpid[1],1,2, switch_dpid[2],3,2, switch_dpid[3],4,2])
s_ct_lsps2 [2].extend([switch_dpid[0], 1,2, switch_dpid[3],1,3, switch_dpid[4],2,3, switch_dpid[2],5,4,switch_dpid[5],2,1, switch_dpid[6],3,2])
'''

adj = defaultdict(lambda:defaultdict(lambda:None))
node_wt = defaultdict(lambda:defaultdict(lambda:None)) 
mac_learning = {}


class ofp_match_withHash(of.ofp_match):
    ##Our additions to enable indexing by match specifications
    @classmethod
    def from_ofp_match_Superclass(cls, other):    
        match = cls()
        
        match.wildcards = other.wildcards
        match.in_port = other.in_port
        match.dl_src = other.dl_src
        match.dl_dst = other.dl_dst
        match.dl_vlan = other.dl_vlan
        match.dl_vlan_pcp = other.dl_vlan_pcp
        match.dl_type = other.dl_type
        match.nw_tos = other.nw_tos
        match.nw_proto = other.nw_proto
        match.nw_src = other.nw_src
        match.nw_dst = other.nw_dst
        match.tp_src = other.tp_src
        match.tp_dst = other.tp_dst
        return match
        
    def __hash__(self):
        return hash((self.wildcards, self.in_port, self.dl_src, self.dl_dst, self.dl_vlan, self.dl_vlan_pcp, self.dl_type, self.nw_tos, self.nw_proto, self.nw_src, self.nw_dst, self.tp_src, self.tp_dst))

class Path(object):
    def __init__(self, src, dst, prev, first_port):
        self.src = src
        self.dst = dst
        self.prev = prev
        self.first_port = first_port
    
    def __repr__(self):
        ret = poxutil.dpid_to_str(self.dst)
        u = self.prev[self.dst]
        while(u != None):
            ret = poxutil.dpid_to_str(u) + "->" + ret
            u = self.prev[u]
        
        return ret            
    
    def _tuple_me(self):
        
        list = [self.dst,]
        u = self.prev[self.dst]
        while u != None:
            list.append(u)
            u = self.prev[u]
        ##log.debug("List path: %s", list)
        ##log.debug("Tuple path: %s", tuple(list))
        return tuple(list)
    
    def __hash__(self):
        return hash(self._tuple_me())
    
    def __eq__(self, other):
        return self._tuple_me() == other._tuple_me()
'''
The following API programs static flows for the cross traffic paths in the network.
'''
   


def gen_random_qual():
    seg_list = []
    new_dict = {}
    post = {}
    for i in range (1,300):
        new = []
        for j in range (1,12):
        #x is result of coin flip
            x = random.randint(0,1)
            new.append(j)
        make_key = str(i)
        new_dict.update({make_key:new})
        seg_list.append(new)
    post.update({"qualities":new_dict})
    return post

'''
The following API implements SABR processing, i.e,computes instantaneous bottleneck bandwidth 
'''
def _forward_path():
    #RO.r('library(forecast)')
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
        client=pymongo.MongoClient("205.172.170.30")
        print( "Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.opencdn
    table = db.portmonitor    
    table1 = db.serv_bandwidth
    best_bw = 100000000000000000.0
    best_serv = 1
    serv_ip = "10.10.10.4"
    serv_index=0
    client_index=0
    hop_count = s_lsps[s_keys[0][0]][1]
    arima_in = []
    print("TRAFFIC_MATRIX \n")
    for i in range(len(s_keys)):  
      for j in range (len(s_keys[i])):
       print s_keys[i][j]
       min_bw=0.0
       for k in range (0,len(s_lsps[s_keys[i][j]][2]),3):
          sum_bw=0.0
          #arima_avg=0.0
          for res in table.find({"dpid": str(s_lsps[s_keys[i][j]][2][k]) , "portno": s_lsps[s_keys[i][j]][2][k+2]}).sort([("_id", pymongo.DESCENDING)]).limit(1):
              #print("MONGO: Value of Search Result:\t")
              #print(res)
              #stat_query = "{\"dpid\":\"" + str(s_lsps[s_keys[i][j]][2][k]) + "\",\"portno\":"+ str(s_lsps[s_keys[i][j]][2][k+1])+"}"
              #opencdn_url = "http://localhost:27080/opencdn/portmonitor/_find?criteria="+urllib.quote(stat_query)+";batch_size=1"
          
              ##print ("ROUTING PYMONGO URL %s", res)
              #stat_resp = requests.get(res)
              ##print("ROUTING stat_query JSON URL %s", stat_resp)
              #s_resp =stat_resp.json()\
              print("ROUTING stat_query JSON URL %s", res)
              if len(res)>0:
                       sum_bw=int(res['TXbytes'])
          #avg_bw=sum_bw/2.0             
          min_bw=max(sum_bw,min_bw)             
      post = {"server_ip": server_list[j],"client_ip": clientip_list[i], "min_bw": (min_bw) , "hop_count": hop_count,  "date": datetime.utcnow()}
       #post.update(post3)
      post_id = table1.insert_one(post).inserted_id           
      s_lsps[s_keys[i][j]][0]= min_bw         
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
       
       
      #print("ROUTING: server is %s and congestion bandwidth is %d", s_keys[i][j], min_bw)                 
      '''
      if best_serv == 0:
        serv_ip = "10.10.10.3"
      elif best_serv == 1:
        serv_ip = "10.10.10.8"
      elif best_serv == 2:
        serv_ip = "10.10.10.16"
      '''
      
       
      '''
       if s_keys[i][j]=="10.10.10.3": 
        post.update(post1)
      elif s_keys[i][j] == "10.10.10.8":
        post.update(post2)  
      else:
        post.update(post3)
      '''
      #post.update(gen_random_qual())
      
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
'''
The following API programs client flows
'''
def _get_path(src, dst):
    #Bellman-Ford algorithm
    keys = switches.keys()
    distance = {}
    previous = {}
    
    for dpid in keys:
        distance[dpid] = float("+inf")
        previous[dpid] = None

    distance[src] = 0
    log.debug("Graph weights randomly assigned:\n")
    for i in range(len(keys)-1):
        for u in adj.keys(): #nested dict
            for v in adj[u].keys():
                w = node_wt[u][v] = random.randrange(1,10)
                log.debug("%d\n"%node_wt[u][v])
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    previous[v] = u 

    for u in adj.keys(): #nested dict
        for v in adj[u].keys():
            w = node_wt[u][v]
            if distance[u] + w < distance[v]:
                log.error("Graph contains a negative-weight cycle")
                return None
    
    first_port = None
    v = dst
    u = previous[v]
    
    while u is not None:
        if u == src:
            first_port = adj[u][v]
        
        
        v = u
        u = previous[v]
        
                
    return Path(src, dst, previous, first_port)  #path
def _install_shortestpath(match):
    try:
        cross_path=s_ct_lsps[(str(match.nw_src),str(match.nw_dst))]
        src = match.nw_src
        dst = match.nw_dst
    except KeyError:
        cross_path=s_ct_lsps[(str(match.nw_dst),str(match.nw_src))]
        src = match.nw_dst
        dst = match.nw_src
    for i in range(0,len(cross_path)-2,3):
        msg = of.ofp_flow_mod()

        msg.match = of.ofp_match(in_port=match.in_port, dl_type =0x0800, nw_src = src, nw_dst = dst)
        msg.idle_timeout = 500
        msg.flags = of.OFPFF_SEND_FLOW_REM    
        msg.actions.append(of.ofp_action_output(port = cross_path[i+1]))
        log.debug("CROSS_TRAFFIC: Installing forward from switch %s to output port %s", cross_path[i], cross_path[i+1])
        poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cross_path[i]),msg)
        
        rev_msg = of.ofp_flow_mod()

        rev_msg.match = of.ofp_match(in_port=cross_path[i+1], dl_type =0x0800, nw_src = dst, nw_dst = src)
        rev_msg.idle_timeout = 500
        rev_msg.flags = of.OFPFF_SEND_FLOW_REM    
        rev_msg.actions.append(of.ofp_action_output(port = cross_path[i+2]))
        log.debug("CROSS_TRAFFIC: Installing reverse from switch %s to output port %s", cross_path[i], cross_path[i+2])
        poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cross_path[i]),rev_msg)
        
        '''
    dst_sw = prev_path.dst
    cur_sw = prev_path.dst
    dst_pck = match.dl_dst
    
    msg = of.ofp_flow_mod()
    #msg.match = match
    
    msg.match = of.ofp_match(in_port=match.in_port, dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)
    msg.idle_timeout = 500
    msg.flags = of.OFPFF_SEND_FLOW_REM    
    msg.actions.append(of.ofp_action_output(port = mac_learning[dst_pck].port))
    log.debug("Installing forward from switch %s to output port %s", poxutil.dpid_to_str(cur_sw), mac_learning[dst_pck].port)
    switches[dst_sw].connection.send(msg)
    
    next_sw = cur_sw
    cur_sw = prev_path.prev[next_sw]
    while cur_sw is not None: #for switch in path.keys():
        msg = of.ofp_flow_mod()
        #msg.match = match
        msg.match = of.ofp_match(in_port = match.in_port,dl_type =0x0800,nw_src = match.nw_src, nw_dst = match.nw_dst)
        msg.idle_timeout = 500
        msg.flags = of.OFPFF_SEND_FLOW_REM
        log.debug("Installing forward from switch %s to switch %s output port %s", poxutil.dpid_to_str(cur_sw), poxutil.dpid_to_str(next_sw), adj[cur_sw][next_sw])
        msg.actions.append(of.ofp_action_output(port = adj[cur_sw][next_sw]))
        switches[cur_sw].connection.send(msg)
        next_sw = cur_sw
        
        cur_sw = prev_path.prev[next_sw]
        '''
        
def _install_shortestpath_arp(match):
    try:
        cross_path=s_ct_lsps[(str(match.nw_src),str(match.nw_dst))]
        src = match.nw_src
        dst = match.nw_dst
    except KeyError:
        cross_path=s_ct_lsps[(str(match.nw_dst),str(match.nw_src))]
        src = match.nw_dst
        dst = match.nw_src
    for i in range(0,len(cross_path)-2,3):
        msg = of.ofp_flow_mod()

        msg.match = of.ofp_match(in_port=match.in_port, dl_type =0x0806, nw_src = src, nw_dst = dst)
        msg.idle_timeout = 500
        msg.flags = of.OFPFF_SEND_FLOW_REM    
        msg.actions.append(of.ofp_action_output(port = cross_path[i+1]))
        log.debug("CROSS_TRAFFIC: Installing forward from switch %s to output port %s", cross_path[i], cross_path[i+1])
        poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cross_path[i]),msg)
        
        rev_msg = of.ofp_flow_mod()

        rev_msg.match = of.ofp_match(in_port=cross_path[i+1], dl_type =0x0806, nw_src = dst, nw_dst = src)
        rev_msg.idle_timeout = 500
        rev_msg.flags = of.OFPFF_SEND_FLOW_REM    
        rev_msg.actions.append(of.ofp_action_output(port = cross_path[i+2]))
        log.debug("CROSS_TRAFFIC: Installing reverse from switch %s to output port %s", cross_path[i], cross_path[i+2])
        poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cross_path[i]),rev_msg)

def _install_arp(conn_dpid, match, init_event, src, ofp_in_port):
    global ct_called
    #log.debug("CROSSTRAFFIC: check port %d", match.tp_dst)
    #log.debug("CROSSTRAFFIC_MATCH: check port %s", match)
    
    #if match.nw_dst == "10.10.10.9" and match.nw_src== "10.10.10.5" and match.nw_src == "10.10.10.4" or match.nw_src == "10.10.10.6" or match.nw_src == "10.10.10.11" or match.nw_src == "10.10.10.7":
    if match.nw_dst in cross_list and match.nw_src in cross_list:
            _install_shortestpath_arp(match)
            log.debug("Calling Cross Traffic %s"%match.nw_src)
            ct_called = True
            return 0
    
    #best_bw=0
    log.debug("****************SOURCE %s and DESTINATION %s******************\n"%(match.nw_src,match.nw_dst))
    #if str(match.nw_src) in client_list and str(match.nw_src) not in server_list:
     # if str(match.nw_dst) not in client_list and str(match.nw_dst) not in server_list:

    print "***************Programmed Path*************\n"
    for i in client_list:
        print i
    if ((match.nw_dst in client_port.keys() and match.nw_src in server_list) or (match.nw_dst in server_list and match.nw_src in client_port.keys())) :
        if match.nw_dst in server_list:
            serv_index = server_list.index(match.nw_dst)
            #print server_list[serv_index]
        elif match.nw_dst in client_port.keys():
            client_index = clientip_list.index((str(match.nw_dst)[0:10]))
            client_ip_new = str(match.nw_dst)
            #print clientip_list[client_index]
        if match.nw_src in server_list:
            serv_index = server_list.index(match.nw_src)
            #print server_list[serv_index]
        elif match.nw_src in client_port.keys():
            client_index = clientip_list.index((str(match.nw_src)[0:10]))
            client_ip_new = str(match.nw_src)
            #print clientip_list[client_index]
        log.debug("Client Index is %d and Server Index is %d and CLient IP %s",client_index,serv_index,client_ip_new)
        best_path = s_keys[client_index][serv_index]
    best_bw = s_lsps[s_keys[client_index][serv_index]][0]
    packet = init_event.parsed
    first_in  = init_event.port
    #s_lsps[best_path][2][2] = client_port[client_ip_new]
    for i in range(0,len(s_lsps[best_path][2])-2,3): #for switch in path.keys():  
        #log.debug("INSTALLING ARP: VALUE OF i %d and Length %d", i, len(s_lsps[best_path][2]))
        cur_sw = s_lsps[best_path][2][i]


        #rev_msg = of.ofp_flow_mod()
        '''
        rev_msg.match = match
        rev_msg.match.nw_dst, rev_msg.match.nw_src = rev_msg.match.nw_src , rev_msg.match.nw_dst
        rev_msg.match.dl_dst, rev_msg.match.dl_src = rev_msg.match.dl_src, rev_msg.match.dl_dst
        rev_msg.match.tp_src, rev_msg.match.tp_dst = rev_msg.match.tp_dst, rev_msg.match.tp_src
        '''
        '''
        if i==0:
            rev_port = first_in
            
            src_sw = "client"
            dst_sw = s_lsps[best_path][2][i]
            msg.match = of.ofp_match(in_port = first_in, dl_type=0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst, tp_src = match.tp_src, tp_dst= match.tp_dst, nw_proto = match.nw_proto)
        
        else:
        '''
        rev_port = s_lsps[best_path][2][i+2]
        #msg.in_port = s_lsps[best_path][2][i+2]
        src_sw = s_lsps[best_path][2][i]
        if i<(len(s_lsps[best_path][2])-3):
            dst_sw = s_lsps[best_path][2][i+3]
        else:
            dst_sw ="last"
        if i==0:
                cl_port=client_port[client_ip_new]
        else:
                cl_port=s_lsps[best_path][2][i+2]
        log.debug("********ARP SRC: %s and ARP DST********** %s",str(match.nw_src),str(match.nw_dst))
        if str(match.nw_src) in client_port.keys():
                msg = of.ofp_flow_mod()
                msg.idle_timeout =10
                msg.flags = of.OFPFF_SEND_FLOW_REM
                msg.match = of.ofp_match(in_port = cl_port,dl_type =0x0806, nw_src = match.nw_src, nw_dst = match.nw_dst)
                log.debug("Installing Forward from switch %s to switch %s: output port %s", src_sw, dst_sw, s_lsps[best_path][2][i+1])
                msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),msg)
                #msg_cl = of.ofp_flow_mod()
                #msg.idle_timeout =10
                #msg.flags = of.OFPFF_SEND_FLOW_REM
                #msg.match = of.ofp_match(in_port = cl_port,dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)
                #log.debug("Installing Forward from switch %s to switch %s: output port %s", src_sw, dst_sw, s_lsps[best_path][2][i+1])
                #msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                #rev_msg.match.in_port = s_lsps[best_path][2][i+1]
        #if src_sw != "client":
                '''
                rev_msg = of.ofp_flow_mod()
                rev_msg.idle_timeout = 10
                rev_msg.flags = of.OFPFF_SEND_FLOW_REM
                rev_msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0806, nw_src = match.nw_dst, nw_dst = match.nw_src)

                rev_msg.out_port = cl_port
                log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, rev_msg.match.in_port,rev_msg.out_port)
                rev_msg.actions.append(of.ofp_action_output(port = cl_port))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
                log.debug("*************ARP CLIENT FLOW: DPID OF CURRENT SWITCH*************%s",cur_sw)
                '''
        elif str(match.nw_dst) in client_port.keys():
                msg = of.ofp_flow_mod()
                msg.idle_timeout = 10
                msg.flags = of.OFPFF_SEND_FLOW_REM
                msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0806, nw_src = match.nw_src, nw_dst = match.nw_dst)

                msg.out_port = cl_port
                log.debug("Installing Reverse1 from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, msg.match.in_port,msg.out_port)
                msg.actions.append(of.ofp_action_output(port = cl_port))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),msg)
                '''
                rev_msg = of.ofp_flow_mod()
                rev_msg.idle_timeout = 10
                rev_msg.flags = of.OFPFF_SEND_FLOW_REM
                rev_msg.match = of.ofp_match(in_port = cl_port,dl_type =0x0806, nw_src = match.nw_dst, nw_dst = match.nw_src)

                rev_msg.out_port = s_lsps[best_path][2][i+1]
                log.debug("Installing Reverse2 from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, rev_msg.match.in_port,rev_msg.out_port)
                rev_msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
                log.debug("*************ARP CLIENT FLOW: DPID OF CURRENT SWITCH*************%s",cur_sw)
                '''
                #rev_msg = of.ofp_flow_mod()
                #rev_msg.idle_timeout = 10
                #rev_msg.flags = of.OFPFF_SEND_FLOW_REM
                #rev_msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)

                #rev_msg.out_port = rev_port
                #log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, rev_msg.match.in_port,rev_msg.out_port)
                #rev_msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+2]))
                #poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
def _install_path(conn_dpid, match, init_event, src, ofp_in_port):
    global ct_called
    #log.debug("CROSSTRAFFIC: check port %d", match.tp_dst)
    #log.debug("CROSSTRAFFIC_MATCH: check port %s", match)
    
    #if match.nw_dst != "10.10.10.3" and match.nw_src== "10.10.10.2" and match.nw_src == "10.10.10.4" or match.nw_src == "10.10.10.6" or match.nw_src == "10.10.10.11" or match.nw_src == "10.10.10.7":
    if match.nw_dst in cross_list and match.nw_src in cross_list:
            _install_shortestpath(match)
            log.debug("Calling Cross Traffic %s"%match.nw_src)
            ct_called = True
            return 0
    
    #best_bw=0
    log.debug("****************SOURCE %s and DESTINATION %s******************\n"%(match.nw_src,match.nw_dst))
    #if str(match.nw_src) in client_list and str(match.nw_src) not in server_list:
     # if str(match.nw_dst) not in client_list and str(match.nw_dst) not in server_list:

    print "***************Programmed Path*************\n"
    for i in client_list:
        print i
    if ((match.nw_dst in client_port.keys() and match.nw_src in server_list) or (match.nw_dst in server_list and match.nw_src in client_port.keys())) :
        if match.nw_dst in server_list:
            serv_index = server_list.index(match.nw_dst)
            #print server_list[serv_index]
        elif match.nw_dst in client_port.keys():
            client_index = clientip_list.index((str(match.nw_dst)[0:10]))
            client_ip_new = str(match.nw_dst)
            #print clientip_list[client_index]
        if match.nw_src in server_list:
            serv_index = server_list.index(match.nw_src)
            #print server_list[serv_index]
        elif match.nw_src in client_port.keys():
            client_index = clientip_list.index((str(match.nw_src)[0:10]))
            client_ip_new = str(match.nw_src)
            #print clientip_list[client_index]
        log.debug("Client Index is %d and Server Index is %d and CLient IP %s",client_index,serv_index,client_ip_new)
        best_path = s_keys[client_index][serv_index]
    best_bw = s_lsps[s_keys[client_index][serv_index]][0]
    '''   
    for j in range (len(s_keys[client_index])):
       print s_keys[i][j] 
       for k in range (len(s_lsps[s_keys[i][j]][2])):
        print s_lsps[s_keys[i][j]][0]
        if best_bw > s_lsps[s_keys[i][j]][0]:
            best_path, best_bw = s_keys[i][j], s_lsps[s_keys[i][j]][0]
       log.debug("BESTPATH: %s and BESTBW = %d", best_path, best_bw)
    '''
    packet = init_event.parsed
    first_in  = init_event.port
    #s_lsps[best_path][2][2] = client_port[client_ip_new]
    for i in range(0,len(s_lsps[best_path][2])-2,3): #for switch in path.keys():  
        #log.debug("INSTALLING : VALUE OF i %d and Length %d", i, len(s_lsps[best_path][2]))
        cur_sw = s_lsps[best_path][2][i]


        #rev_msg = of.ofp_flow_mod()
        '''
        rev_msg.match = match
        rev_msg.match.nw_dst, rev_msg.match.nw_src = rev_msg.match.nw_src , rev_msg.match.nw_dst
        rev_msg.match.dl_dst, rev_msg.match.dl_src = rev_msg.match.dl_src, rev_msg.match.dl_dst
        rev_msg.match.tp_src, rev_msg.match.tp_dst = rev_msg.match.tp_dst, rev_msg.match.tp_src
        '''
        '''
        if i==0:
            rev_port = first_in
            
            src_sw = "client"
            dst_sw = s_lsps[best_path][2][i]
            msg.match = of.ofp_match(in_port = first_in, dl_type=0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst, tp_src = match.tp_src, tp_dst= match.tp_dst, nw_proto = match.nw_proto)
        
        else:
        '''
        #msg.in_port = s_lsps[best_path][2][i+2]
        src_sw = s_lsps[best_path][2][i]
        if i<(len(s_lsps[best_path][2])-3):
            dst_sw = s_lsps[best_path][2][i+3]
        else:
            dst_sw ="last"
        if i==0:
                cl_port=client_port[client_ip_new]
        else:
                cl_port=s_lsps[best_path][2][i+2]
        if str(match.nw_src) in client_port.keys():
                msg = of.ofp_flow_mod()
                msg.idle_timeout =10
                msg.flags = of.OFPFF_SEND_FLOW_REM
                msg.match = of.ofp_match(in_port = cl_port,dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)
                log.debug("Installing Forward from switch %s to switch %s: output port %s", src_sw, dst_sw, s_lsps[best_path][2][i+1])
                msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                #rev_msg.match.in_port = s_lsps[best_path][2][i+1]
        #if src_sw != "client":
                log.debug("*************CLIENT FLOW: DPID OF CURRENT SWITCH*************%s",cur_sw)
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),msg)
                '''
                rev_msg = of.ofp_flow_mod()
                rev_msg.idle_timeout = 10
                rev_msg.flags = of.OFPFF_SEND_FLOW_REM
                rev_msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0800, nw_src = match.nw_dst, nw_dst = match.nw_src)

                rev_msg.out_port = cl_port
                log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, msg.match.in_port,msg.out_port)
                rev_msg.actions.append(of.ofp_action_output(port = cl_port))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
                '''
        elif str(match.nw_dst) in client_port.keys():
                msg = of.ofp_flow_mod()
                msg.idle_timeout = 10
                msg.flags = of.OFPFF_SEND_FLOW_REM
                msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)

                msg.out_port =cl_port
                log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, msg.match.in_port, msg.out_port)
                msg.actions.append(of.ofp_action_output(port = cl_port))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),msg)
                '''
                rev_msg = of.ofp_flow_mod()
                rev_msg.idle_timeout = 10
                rev_msg.flags = of.OFPFF_SEND_FLOW_REM
                rev_msg.match = of.ofp_match(in_port = cl_port,dl_type =0x0800, nw_src = match.nw_dst, nw_dst = match.nw_src)

                rev_msg.out_port = s_lsps[best_path][2][i+1]
                log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, msg.match.in_port,msg.out_port)
                rev_msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
                '''
        '''
        #elif str(match.nw_src) in server_list:
                msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+1],dl_type =0x0800, nw_src = match.nw_src, nw_dst = match.nw_dst)
                log.debug("Installing Forward from switch %s to switch %s: output port %s", src_sw, dst_sw, s_lsps[best_path][2][i+2])
                msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+2]))
                #rev_msg.match.in_port = s_lsps[best_path][2][i+1]
        #if src_sw != "client":
                log.debug("*************SERVER FLOW: DPID OF CURRENT SWITCH*************%s",cur_sw)
                poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),msg)
                
                #rev_msg.match = of.ofp_match(in_port = s_lsps[best_path][2][i+2] ,dl_type =0x0800, nw_src = match.nw_dst, nw_dst = match.nw_src, nw_proto = match.nw_proto)            
                #rev_msg.out_port = s_lsps[best_path][2][i+1]
                #log.debug("Installing Reverse from switch %s to switch %s : input port %s and output port %s", src_sw, dst_sw, rev_msg.match.in_port,  s_lsps[best_path][2][i+2])
                #rev_msg.actions.append(of.ofp_action_output(port = s_lsps[best_path][2][i+1]))
                #poxcore.openflow.sendToDPID(poxutil.str_to_dpid(cur_sw),rev_msg)
        '''
class NewFlow(Event):
    def __init__(self, prev_path, match, rev_match):
        Event.__init__(self)
        self.match = match
        self.prev_path = prev_path
        self.rev_match = rev_match
     
    
class Switch(EventMixin):
    _eventMixin_events = set([
                            NewFlow,
                            ])
    def __init__(self, connection, l3_matching=False):
        self.connection = connection
        self.l3_matching = l3_matching
        connection.addListeners(self)
        for p in self.connection.ports.itervalues(): #Enable flooding on all ports until they are classified as links
            self.enable_flooding(p.port_no)
    
    def __repr__(self):
        return poxutil.dpid_to_str(self.connection.dpid) 
    
    
    def disable_flooding(self, port):
        msg = of.ofp_port_mod(port_no = port,
                        hw_addr = self.connection.ports[port].hw_addr,
                        config = of.OFPPC_NO_FLOOD,
                        mask = of.OFPPC_NO_FLOOD)
    
        self.connection.send(msg)
    

    def enable_flooding(self, port):
        msg = of.ofp_port_mod(port_no = port,
                            hw_addr = self.connection.ports[port].hw_addr,
                            config = 0, # opposite of of.OFPPC_NO_FLOOD,
                            mask = of.OFPPC_NO_FLOOD)
    
        self.connection.send(msg)
    
    def _handle_PacketIn(self, event):
        def forward(port):
            """Tell the switch to drop the packet"""
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = port))    
            if event.ofp.buffer_id is not None:
                msg.buffer_id = event.ofp.buffer_id
            else:
                msg.data = event.ofp.data
            msg.in_port = event.port
            self.connection.send(msg)
                
        def flood():
            """Tell all switches to flood the packet, remember that we disable inter-switch flooding at startup"""
            #forward(of.OFPP_FLOOD)
            for (dpid,switch) in switches.iteritems():
                msg = of.ofp_packet_out()
                if switch == self:
                    if event.ofp.buffer_id is not None:
                        msg.buffer_id = event.ofp.buffer_id
                    else:
                        msg.data = event.ofp.data
                    msg.in_port = event.port
                else:
                    msg.data = event.ofp.data
                ports = [p for p in switch.connection.ports if (dpid,p) not in switch_ports]
                if len(ports) > 0:
                    for p in ports:
                        msg.actions.append(of.ofp_action_output(port = p))
                    switches[dpid].connection.send(msg)
                
                
        def drop():
            """Tell the switch to drop the packet"""
            if event.ofp.buffer_id is not None: #nothing to drop because the packet is not in the Switch buffer
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id 
                event.ofp.buffer_id = None # Mark as dead, copied from James McCauley, not sure what it does but it does not work otherwise
                msg.in_port = event.port
                self.connection.send(msg)
        
        #log.debug("Received PacketIn")        
        packet = event.parsed
                
        SwitchPort = namedtuple('SwitchPoint', 'dpid port')
        
        if (event.dpid,event.port) not in switch_ports:                        # only relearn locations if they arrived from non-interswitch links
            mac_learning[packet.src] = SwitchPort(event.dpid, event.port)    #relearn the location of the mac-address
        
        if packet.effective_ethertype == packet.LLDP_TYPE:
            drop()
            #log.debug("Switch %s dropped LLDP packet", self)
        elif packet.dst.is_multicast:
            flood()
            #log.debug("Switch %s flooded multicast 0x%0.4X type packet", self, packet.effective_ethertype)
        elif packet.dst not in mac_learning:
            flood() #Let's first learn the location of the recipient before generating and installing any rules for this. We might flood this but that leads to further complications if half way the flood through the network the path has been learned.
            #log.debug("Switch %s flooded unicast 0x%0.4X type packet, due to unlearned MAC address", self, packet.effective_ethertype)
        elif packet.effective_ethertype == packet.ARP_TYPE:
            #These packets are sent so not-often that they don't deserve a flow
            #Instead of flooding them, we drop it at the current switch and have it resend by the switch to which the recipient is connected.
            #flood()
            match = ofp_match_withHash.from_packet(packet)
            log.debug("PrintARPSource%s",str(match.nw_src))
            _install_arp(self.connection.dpid, match, event, packet.src,event.ofp.in_port)
            '''
            drop()
            dst = mac_learning[packet.dst]
            msg = of.ofp_packet_out()
            msg.data = event.ofp.data
            msg.actions.append(of.ofp_action_output(port = dst.port))
            switches[dst.dpid].connection.send(msg)
            
            
            dst = mac_learning[packet.dst]
            log.debug("Switch %s processed unicast ARP (0x0806) packet, send to recipient by switch %s", self, poxutil.dpid_to_str(dst.dpid))
            '''
        else:
            if packet.type == packet.IP_TYPE:
                log.debug("Switch %s received PacketIn of type 0x%0.4X, received from %s.%s", self, packet.effective_ethertype, poxutil.dpid_to_str(event.dpid), event.port)
                if packet.find("ipv4").srcip not in server_list and packet.find("ipv4").srcip not in client_list and packet.find("ipv4").srcip not in cross_list: 
                    print packet.find("ipv4").srcip
                if packet.find("ipv4").dstip not in server_list and packet.find("ipv4").dstip not in client_list and packet.find("ipv4").dstip not in cross_list:
                    client_list.append(packet.find("ipv4").dstip)
                    print packet.find("ipv4").dstip
            dst = mac_learning[packet.dst]

            if self.l3_matching == True: #only match on l2-properties, useful when doing experiments with UDP streams as you can insert a flow using ping and then start sending udp.
            #if match.nw_src == "10.10.10.14" or match.nw_src== "10.10.10.2" or match.nw_src == "10.10.10.4" or match.nw_src == "10.10.10.6" or match.nw_src == "10.10.10.11" or match.nw_src == "10.10.10.7":    
                match = ofp_match_withHash()
                rev_match = ofp_match_withHash()
                match.dl_src =rev_match.dl_dst = packet.src
                match.dl_dst = rev_match.dl_src =  packet.dst
                match.dl_type = rev_match.dl_type = packet.type
                p = packet.next
                if isinstance(p, vlan):
                    match.dl_type = rev_match.dl_type = p.eth_type
                    match.dl_vlan = rev_match.dl_vlan = p.id
                    match.dl_vlan_pcp = rev_match.dl_vlan_pcp =p.pcp
                    p = p.next
                if isinstance(p, ipv4):
                    match.nw_src = rev_match.nw_dst = p.srcip
                    match.nw_dst = rev_match.nw_src = p.dstip
                    match.nw_proto = rev_match.nw_proto = p.protocol
                    match.nw_tos = rev_match.nw_tos = p.tos
                    p = p.next
                else:
                    match.dl_vlan = rev_match.dl_vlan= of.OFP_VLAN_NONE
                    match.dl_vlan_pcp = rev_match.dl_vlan = 0
                log.debug("L3 packet MATCHED\n")
                #_install_path(match, event)    
                
            else:
                match = ofp_match_withHash.from_packet(packet)
                rev_match = match
                
            
            _install_path(self.connection.dpid, match, event, packet.src,event.ofp.in_port)
            
            #forward the packet directly from the last switch, there is no need to have the packet run through the complete network.
            
            drop()
            dst = mac_learning[packet.dst]
            msg = of.ofp_packet_out()
            msg.data = event.ofp.data
            msg.actions.append(of.ofp_action_output(port = dst.port))
            #log.debug("Switch %s processed unicast 0x%0.4x type packet, send to recipient by switch %s", self, packet.effective_ethertype, poxutil.dpid_to_str(dst.dpid))
            switches[dst.dpid].connection.send(msg)
            #self.raiseEvent(NewFlow(rev_match, match, Path(msg.in_port, msg.out_port, , first_port)))
            ##log.debug("Switch %s processed unicast 0x%0.4x type packet, send to recipient by switch %s", self, packet.effective_ethertype, poxutil.dpid_to_str(dst.dpid))
            
        
    def _handle_ConnectionDown(self, event):
        #log.debug("Switch %s going down", poxutil.dpid_to_str(self.connection.dpid))
        del switches[self.connection.dpid]
        #pprint(switches)

        
class NewSwitch(Event):
    def __init__(self, switch):
        Event.__init__(self)
        self.switch = switch

class Forwarding(EventMixin):
    _core_name = "opennetmon_forwarding" # we want to be poxcore.opennetmon_forwarding
    _eventMixin_events = set([NewSwitch,])
    
    def __init__ (self, l3_matching):
        #log.debug("Forwarding coming up")
                
        def startup():
            poxcore.openflow.addListeners(self)
            poxcore.openflow_discovery.addListeners(self)
            poxcore.openflow.miss_send_len = 65535
            #log.debug("Forwarding started")
        
        self.l3_matching = l3_matching
        poxcore.call_when_ready(startup, 'openflow', 'openflow_discovery')
        
            
    def _handle_LinkEvent(self, event):
        link = event.link
        if event.added:
            #log.debug("Received LinkEvent, Link Added from %s to %s over port %d", poxutil.dpid_to_str(link.dpid1), poxutil.dpid_to_str(link.dpid2), link.port1)
            adj[link.dpid1][link.dpid2] = link.port1
            switch_ports[link.dpid1,link.port1] = link
            #switches[link.dpid1].disable_flooding(link.port1)
            #pprint(adj)
        else:
            log.debug("Received LinkEvent, Link Removed from %s to %s over port %d", poxutil.dpid_to_str(link.dpid1), poxutil.dpid_to_str(link.dpid2), link.port1)
            ##Disabled those two lines to prevent interference with experiment due to falsely identified disconnected links.
            #del adj[link.dpid1][link.dpid2]
            #del switch_ports[link.dpid1,link.port1]
            
            
            #switches[link.dpid1].enable_flooding(link.port1)
            
        
        self._calc_ForwardingMatrix()
        
    def _calc_ForwardingMatrix(self):
        print("Calculating forwarding matrix")
        
    def _handle_ConnectionUp(self, event):
        sw = Switch(event.connection, l3_matching=self.l3_matching)
        switches[event.dpid] = sw;
        self.raiseEvent(NewSwitch(sw))
        #log.debug("New switch connection: %s", event.connection)

def create_matrix ():
    log.debug("Child process called\n-------------------")
    #_forward_path
    time.sleep(5)
    t = Timer(2.0, _forward_path, recurring=True)
    #t = threading.Timer(5.0, _forward_path)
    #threads.append(t)
    #t.daemon = True
    t.start()
    time.sleep(5)
    #return 0

        
def launch (l3_matching=False):
    #threads =[]
    
    poxcore.registerNew(Forwarding, l3_matching)
    
    #time.sleep(10)
    #post2=gen_random_qual()
    print "Calling Timer\n"
    #t = Timer(5.0, _forward_path, recurring=True)
    #t.daemon = True
    #t.start()
    #t.start()
    #thread.start_new_thread(create_matrix, ())
    #poxcore.registerNew(create_matrix)
    '''
    t=Timer(5.0, _forward_path, recurring=True)
    t.daemon = True
    t.start()
    '''
    '''
    p = Process(name='daemon', target=create_matrix)
    p.daemon = True
    p.start()
    #p.join()
    '''    
    #t = threading.Timer(5.0, _forward_path)
    #threads.append(t)
    #t.daemon = True
    #t.start()
    
  