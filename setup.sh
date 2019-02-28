#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_9_4_13
cd CMSSW_9_4_13/src
eval `scramv1 runtime -sh`
cd -
xrdcp root://cmsxrootd.fnal.gov//store/user/arizzi/Nano01Fall17/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X-Nano01Fall17/180214_161216/0000/test94X_NANO_1.root .

