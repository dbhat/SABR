#!/usr/bin/env python
'''
This is a Python script which is used to automate AStream client and
cross traffic generators for SABR evaluation.
'''
from fabric.api import *
import random

import socket
socket.setdefaulttimeout(5)

import numpy as np
from scipy.stats import zipf
import random 
import bisect 
import math 


import subprocess 
import paramiko
import pymongo
from pymongo import MongoClient
import logging
logging.basicConfig()
import sys
import threading
import os
import time
from collections import defaultdict
user="dbhat0"

MAX_TRIALS = 1
zipf_dist = dict()
client_ip = ["clnode080.clemson.cloudlab.us","clnode064.clemson.cloudlab.us", "clnode064.clemson.cloudlab.us","clnode064.clemson.cloudlab.us","clnode057.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode059.clemson.cloudlab.us","clnode059.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode047.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode096.clemson.cloudlab.us"]
client_ports = [30267, 30274, 30273, 30275, 30273,30270,30271,30270,30271,30272,30267,30270,30271,30272,30268,30271,30272,30273,30273,30274]
client_hosts_zipf = ["clnode080.clemson.cloudlab.us","clnode064.clemson.cloudlab.us", "clnode064.clemson.cloudlab.us","clnode064.clemson.cloudlab.us","clnode057.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode059.clemson.cloudlab.us","clnode059.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode047.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode096.clemson.cloudlab.us","clnode096.clemson.cloudlab.us"]
server_ip=["clnodevm064-1.clemson.cloudlab.us","clnodevm064-2.clemson.cloudlab.us","clnodevm059-1.clemson.cloudlab.us","clnodevm096-1.clemson.cloudlab.us"]
client_hosts =[]

client_hosts1 = ["clnode054.clemson.cloudlab.us","clnode068.clemson.cloudlab.us","clnode068.clemson.cloudlab.us","clnode054.clemson.cloudlab.us","clnode054.clemson.cloudlab.us"]
client_hosts2 = ["clnode082.clemson.cloudlab.us","clnode082.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode082.clemson.cloudlab.us","clnode082.clemson.cloudlab.us"]
client_hosts3 = ["clnode080.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode080.clemson.cloudlab.us","clnode051.clemson.cloudlab.us","clnode082.clemson.cloudlab.us"]
client_hosts4 = ["clnode068.clemson.cloudlab.us","clnode051.clemson.cloudlab.us","clnode068.clemson.cloudlab.us","clnode068.clemson.cloudlab.us","clnode068.clemson.cloudlab.us"]
#cl_comm =["\"cd /users/dbhat0/AStream; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p sara > /dev/null &\"","\"cd /users/dbhat0/astream_dash_clab; python dist/client/dash_client_cachemap.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p vlc > /users/dbhat0/dash_"+str(ipaddress).replace(".","")+"2>&1\""]

def gen_zipf(a,n):
    s= np.random.zipf(a,n)
    result = (s/float(max(s)))*n
    return np.floor(result)

def dash_server(ipaddress,run):
    global user
     
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress,username=user,password="Platinum*1989",key_filename="/users/dbhat/.ssh/id_geni_ssh_rsa")
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception! ..."      
         
    except paramiko.SSHException:
        print "[-] SSH Exception! ..." 
         
    works = ipaddress.strip('\n')+','+user  
    print '[+] '+ works
    if run == 0:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus saradump/cachestatus/cache1.bson")
    elif run == 1:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus sabrdump/cachestatus/cache1.bson")
	elif cl_comm == 2:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus squaddump/cachestatus/cache1.bson")    	
    elif cl_comm == 3:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus squad_sabrdump2/cachestatus/cache1.bson")
    elif cl_comm == 4:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus boladump2/cachestatus/cache1.bson")
    elif cl_comm == 5:
		stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus sabrboladump2/cachestatus/cache1.bson")

    print stdout.read()						
    print stderr.read()
    ssh.close()

def dash_client(ipaddress, ports, zipf_index, mpd_ip, cl_comm):
    global user
     
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress,username=user,port=ports,password="Platinum*1989",key_filename="/users/dbhat/.ssh/id_geni_ssh_rsa")
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception! ..."      
         
    except paramiko.SSHException:
        print "[-] SSH Exception! ..." 
         
    works = ipaddress.strip('\n')+','+user  
    print '[+] '+ works
    s = zipf_dist[ipaddress][zipf_index]
    if cl_comm == 0:
    	cl_command = "cd /users/dbhat0/AStream; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p sara > /dev/null &"
    elif cl_comm == 1:
    	cl_command = "cd /users/dbhat0/astream_dash_clab; python dist/client/dash_client_cachemap.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p vlc > /users/dbhat0/dash_"+str(ipaddress).replace(".","")+"2>&1"
	elif cl_comm == 2:
		cl_command = "cd /users/dbhat0/AStream_SQUAD; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p empirical > /dev/null &"
    elif cl_comm == 3:
		cl_command = "cd /users/dbhat0/astream_dash_squad; python dist/client/dash_client_cachemap.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p empirical > /users/dbhat0/dash_"+str(ipaddress).replace(".","")+"2>&1"
	elif cl_comm == 4:
		cl_command = "cd /users/dbhat0/astream_dash_bola; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p bola > /dev/null &"
    elif cl_comm == 5:
		cl_command = "cd /users/dbhat0/astream_sabr_bola; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p bola > /dev/null &"
    
    #cl_command="rm /users/dbhat0/astream_sabr_bola/ASTREAM_LOGS/*; rm /users/dbhat0/astream_dash_bola/ASTREAM_LOGS/*; rm /users/dbhat0/astream_dash_clab/ASTREAM_LOGS/*; rm /users/dbhat0/AStream/ASTREAM_LOGS/*; rm /users/dbhat0/astream_dash_squad/ASTREAM_LOGS/*;rm /users/dbhat0/AStream_SQUAD/ASTREAM_LOGS/*"
    stdin,stdout,stderr=ssh.exec_command(cl_command)
    stringout = str(stderr.readlines()) + str(ipaddress) + str(ports)
    print stringout
    
    #print stdout.readlines()
    ssh.close()

    
if __name__ == "__main__": 
 for run in range (0,6):
 	for ip in server_ip:	
		try:
				client=pymongo.MongoClient(ip)#Replace with IP of specific server
				print"Connected successfully again!!!"
		except pymongo.errors.ConnectionFailure, e:
				print "Could not connect to MongoDB sadly"
		db = client.cachestatus
		table = db.cache1
		table.delete_many({})
		dash_server(str(ip),run)
	try:
	    
	        for client in client_hosts_zipf:
			zipf_dist[client] = gen_zipf(2,49)
			print zipf_dist[client], client

		
	    	zipf_index=0
	    	for no_of_trials in range(MAX_TRIALS):
				for repeat in range(4):
							 count=0
							 while count<len(client_ip):
									concat=str(client_ip[count])
									if (concat in client_hosts1) and ((count%2)==0):
											mpd_ip = "10.10.10.4"
									elif (concat in client_hosts2) and ((count%2)!=0):
											mpd_ip = "10.10.10.16"
									elif (concat in client_hosts3) and ((count%2)==0):
											mpd_ip = "10.10.10.12"
									elif (concat in client_hosts4) and ((count%2)!=0):
											mpd_ip = "10.10.10.27"
									else:
											mpd_ip = "10.10.10.1"

									threading.Thread(target=dash_client,args=(concat,client_ports[count],zipf_index,mpd_ip,run)).start()
									time.sleep(1)
									count+=1
							 time.sleep(3)
							 zipf_index+=1
				time.sleep(310.0)
				if zipf_index>=43:
					zipf_index=0
					for client in range(0,len(client_hosts_zipf)):
							str_zipf= str(client_hosts_zipf[client])+str(client_ports[client])
							zipf_dist[str_zipf] = zipf_collect[z_index]
							print zipf_dist[str_zipf], client
							z_index+=1
	    
	    
        
 	   
	except Exception, e:
		print '[-] General Exception'
	
	    
    	
	
