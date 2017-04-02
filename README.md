# SABR
This repo contains all source code for implementing network assisted adaptive bitrate video streaming and evaluating the system in the CloudLab testbed

## About this system
This system has been tested and evaluated in [CloudLab](https://www.cloudlab.us/), a testbed for researchers to build and test clouds and new architectures.
In order to experiment with CloudLab, you will need an account for access and a profile to instantiate. The profile is specified here as <i>cloudlab_topo.rspec</i>

The following subsystems are included:

## A. Controller and SABR

### Pre-requisites
This component has been tested on a server that runs Ubuntu 14.04 and has the following dependencies:

* [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
* OpenNetMon - included in this directory and requires the [PoX controller](https://github.com/noxrepo/pox)
* [R for Ubuntu](https://cran.r-project.org/bin/linux/ubuntu/README.html)
* [Forecast package in R](https://cran.r-project.org/web/packages/forecast/forecast.pdf)
* [rpy2](https://rpy2.readthedocs.io/en/version_2.8.x/) - This is the python library used to invoke R functions like ARIMA from Python.

### Prepare environment and run
1. You will need to setup 3 tables in a MongoDB database; portmonitor, serv_bandwidth, cachemiss where portmonitor will be used to archive network port statistics on active downstream paths, serv_bandwidth is used to store the processed ARIMA forecasts along with cache status and cachemiss is used to archive the incoming cache misses to be used for content placement for various strategies, respectively. For portmonitor and serv_bandwidth tables, you may need to set the maximum size limit using capped collections as specified [here.](https://docs.mongodb.com/manual/core/capped-collections/) For the cachemiss table, it is mandatory to enable capped collections in order for the caching functionality to work. 
2. Run the controller
3. Run ARIMA forecast and cache status collection module
4. Run the caching component - For the initial setup of the empty caches, this script must be run only after the orchestration of the testbed experiments has started.

## B. Orchestration - Run experiments on CloudLab testbed.
1. Setup Switches - Create OVS bridges and connect to the controller IP above. The script, <i>automate_sabr_clab.py</i>, can be updated to remotely execute on switches if desired.
2. The script, <i>automate_sabr_clab.py</i> maybe used to automate experiment runs on CloudLab using remote login capability provided by the Python-based [Paramiko](http://www.paramiko.org/) library. The script mainly does the following:
  
    a. Run client algorithm using AStream
  
    b. Resets MongoDB caches for each run/set of runs

3. To run this script on your machine ensure that:

    a. The following Python libraries are installed: numpy, scipy, paramiko, pymongo
  
    b. Copy your SSH keys locally and provide the login credentials in the <i>automate_sabr_clab.py</i> script.
  
    c. Replace the server and client lists with login information in <i>automate_sabr_clab.py</i>.

## C. Parsing - Collect and Analyze Results
1. A sample BASH script,<i>getmultipleruns_BOLA.sh</i>, is provided to collect the results from the CloudLab client machines. This script retrieves results from 60 clients and saves them in different folders to be parsed. You will need to update it with login information of your CloudLab clients. For every algorithm, replace the default, BOLAO, with the name of the client algorithm.
2. For parsing results and computing QoE metrics, average quality bitrate, number of quality switches, spectrum and rebuffering ratio, <i>matplotlib_clab.py</i>, may be used. The script contains parsing logic for BOLAO and BOLAO with SABR. You will need to replace BOLAO with paths for other algorithm results.
3. Cache hit-rates can be computed using the script, <i>cdf_hitratio_qual.py</i>. The current example contains parsing script for BOLAO for the Quality-based caching case. You will need to replace this with other content placement result folders for the Global and Local caching cases.
4. Total content requests per quality can be obtained using the script, <i>cdf_hitratio_qual.py</i>, for BOLAO and SQUAD for the Quality-based caching case. You will need to replace this with other content placement result folders for the Global and Local caching cases.
## D. MATLAB - plotting scripts
