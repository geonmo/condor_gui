#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_7_6_6
cd CMSSW_7_6_6/src
eval `scramv1 runtime -sh`
cd -
root -l -b -q "run.C(\"$1\")"
