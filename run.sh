#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_10_2_9
cd CMSSW_10_2_9/src
eval `scramv1 runtime -sh`
cd -
echo $(hostname)
pwd
cp x509* /tmp
voms-proxy-info -all
./getZMass.py $1
