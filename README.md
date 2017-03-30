# SABR
This repo contains all source code for implementing network assisted adaptive bitrate video streaming and evaluating the system in the CloudLab testbed

## About this system
This system has been tested and evaluated in [CloudLab](https://www.cloudlab.us/), a testbed for researchers to build and test clouds and new architectures.
In order to experiment with CloudLab, you will need an account for access and a profile to instantiate. The profile is specified here as <i>cloudlab_topo.rspec</i>

The following subsystems are included:

## 1. Controller and SABR

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

## 2. Orchestration - Run experiments on CloudLab testbed.

## 3. Parsing - Collect and Analyze Results

## 4. MATLAB - plotting scripts
