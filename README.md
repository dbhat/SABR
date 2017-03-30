# SABR
This repo contains all source code for implementing network assisted adaptive bitrate video streaming and evaluating the system in the CloudLab testbed

## About this system
This system has been tested and evaluated in [CloudLab](https://www.cloudlab.us/), a testbed for researchers to build and test clouds and new architectures.
In order to experiment with CloudLab, you will need an account for access and a profile to instantiate. The profile is specified here as <i>cloudlab_topo.rspec</i>

The following subsystems are included:

## Controller and SABR

### Pre-requisites
This component has been tested on a server that runs Ubuntu 14.04 and has the following dependencies:

1. [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
2. OpenNetMon - included in this directory and requires the [PoX controller](https://github.com/noxrepo/pox)
3. [R for Ubuntu](https://cran.r-project.org/bin/linux/ubuntu/README.html)
4. [Forecast package in R](https://cran.r-project.org/web/packages/forecast/forecast.pdf)
5. [rpy2](https://rpy2.readthedocs.io/en/version_2.8.x/) - This is the python library used to invoke R functions like ARIMA from Python.

## Orchestration - Run experiments on CloudLab testbed

## Parsing - Collect and Analyze Results

## MATLAB - plotting scripts
