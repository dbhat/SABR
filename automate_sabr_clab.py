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
        ssh.connect(ipaddress,username=user,password=<password for CloudLab key goes here>,key_filename=<<Path to SSH key>>)
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception! ..."

    except paramiko.SSHException:
        print "[-] SSH Exception! ..."

    works = ipaddress.strip('\n')+','+user
    print '[+] '+ works
    stdin,stdout,stderr=ssh.exec_command("mongorestore --collection cache1 --db cachestatus bolaodump/cachestatus/cache1.bson")

    print stdout.read()
    print stderr.read()
    ssh.close()
'''
    This API is used to run different clients with and without SABR modifications
'''
def dash_client(ipaddress, ports, zipf_index, mpd_ip):
    global user
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress,username=user,port=ports,password="<CloudLab Password>",key_filename="<Path to SSH key>")
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception! ..."      
         
    except paramiko.SSHException:
        print "[-] SSH Exception! ..." 
         
    works = ipaddress.strip('\n')+','+user  
    print '[+] '+ works
    #Insert relevant player command here
    cl_command = "cd /users/dbhat0/astream_dash_bolao; python dist/client/dash_client.py -m http://"+str(mpd_ip)+"/BigBuckBunny_2s_mod" + str(int(s)+1) + "/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/BigBuckBunny_2s_mod" +str(int(s)+1)+ ".mpd -p bola > /dev/null &"    stringerr = str(stderr.readlines()[1:]) + str(ipaddress) + str(ports)
    stdin,stdout,stderr=ssh.exec_command(cl_command)
    stringout = str(stderr.readlines()) + str(ipaddress) + str(ports)
    print stringout
    ssh.close()

if __name__ == "__main__": 

	
	try:
	    
	    for client in client_hosts_zipf:
			zipf_dist[client] = gen_zipf(2,49)
			print zipf_dist[client], client

        #Enable to reset cache
        '''
	    count=0
	    while count<len(server_ip):
	    	concat=str(server_ip[count])
	    	threading.Thread(target=dash_server,args=(concat,)).start()
	    	count+=1
	    '''
	    
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
					
					threading.Thread(target=dash_client,args=(concat,client_ports[count],zipf_index,mpd_ip)).start()
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
                    z_index+=1

	except Exception, e:
		print '[-] General Exception'
	
