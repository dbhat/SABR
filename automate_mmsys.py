#!/usr/bin/env python
'''
This is a Python script which is used to automate AStream clients for SABR evaluation.
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
user = <user name for cloudlab>
MAX_TRIALS = <Integer of no. of experiments>
zipf_dist = dict()
client_ip=[<list of client IPs>]
client_ports = [<list of client ports>]
client_hosts_zipf = [<list of client IPs>]
server_ip=[<list of server IPs>]
client_hosts =[]

client_hosts1 = [<list of client IPs Group A>]
client_hosts2 = [<list of client IPs Group B>]
client_hosts3 = [<list of client IPs Group C>]
client_hosts4 = [<list of client IPs Group D>]

def gen_zipf(a,n):
    s= np.random.zipf(a,n)
    result = (s/float(max(s)))*n
    return np.floor(result)
'''
This API is used to reset caches before every run
'''
def dash_server(ipaddress,run):
    global user
     
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress,username=user,password=<password for CloudLab key goes here>,key_filename=<path to ssh key>)
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
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus squad_sabrdump/cachestatus/cache1.bson")
    elif cl_comm == 4:
    	stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus boladump/cachestatus/cache1.bson")
    elif cl_comm == 5:
		stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus sabrboladump/cachestatus/cache1.bson")

    print stdout.read()						
    print stderr.read()
    ssh.close()

'''
    This API is used to run different clients with and without SABR modifications
'''
def dash_client(ipaddress, ports, zipf_index, mpd_ip, cl_comm):
    global user
     
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress,username=user,port=ports,password=<password for CloudLab key goes here>,key_filename=<path to ssh key>)
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

    stdin,stdout,stderr=ssh.exec_command(cl_command)
    stringout = str(stderr.readlines()) + str(ipaddress) + str(ports)
    print stringout
    
    #print stdout.readlines()
    ssh.close()

    
if __name__ == "__main__": 
 for run in range (0,6):
 	for ip in server_ip:	
		try:
				client=pymongo.MongoClient(ip)
				print"Connected successfully again!!!"
		except pymongo.errors.ConnectionFailure, e:
				print "Could not connect to MongoDB sadly"
		db = client.cachestatus
		table = db.cache1
        table.delete_many({})#Reset caches before each run
		dash_server(str(ip),run)
	try:
            #Client chooses video from a set of 50 using the zipf distribution
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
	
	    
    	
	
