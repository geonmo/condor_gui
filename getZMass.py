#!/usr/bin/env python

import ROOT
import os, sys
from LFNTool import SearchROOT


verbose = False
def getZMass(argv):
    infile = argv[1]
    print("Searching input root file...")
    searcher= SearchROOT()
    searcher.verboseOn()
    infilePFN = searcher.fromLFN(infile).toPFN()
    print("Load ROOTFile : "+infilePFN)
    try:
        inROOTFile = ROOT.TFile.Open(infilePFN)
        if(inROOTFile == None) : raise Exception("NoFile")
    except :
        print("file is missing or not accessible.")
        return(-1)
    tree = inROOTFile.Events
    zcandMass =[]
    for nevent, event in enumerate(tree):
        if (nevent >10000) : break
        muon_tlorentz=[]
        muon_charge=[]
        elec_tlorentz=[]
        elec_charge=[]


        if(verbose): print ("Num. of Events : ",event.event)
        if(verbose): print ("Num. of Muon : ",event.nMuon)
        for i_muon in range(event.nMuon):
            #print (event.Muon_pt[i_muon])
            muon_charge.append(event.Muon_charge[i_muon])
            muon_tlv = ROOT.TLorentzVector()
            muon_tlv.SetPtEtaPhiM(event.Muon_pt[i_muon], event.Muon_eta[i_muon],
                    event.Muon_phi[i_muon], 0.105)
            muon_tlorentz.append(muon_tlv)
        if(verbose): print ("Num. of Electron : ",event.nElectron)
        for i_elec in range(event.nElectron):
            #print (event.Electron_pt[i_elec])
            elec_charge.append(event.Electron_charge[i_elec])
            elec_tlv = ROOT.TLorentzVector()
            elec_tlv.SetPtEtaPhiM(event.Electron_pt[i_elec], event.Electron_eta[i_elec],
                    event.Electron_phi[i_elec], 0.511*0.001)
            elec_tlorentz.append(elec_tlv)


        for i in range(len(muon_charge)-1):
            charge_first = muon_charge[i]
            for j in range(len(muon_charge))[i+1:]:
                charge_second = muon_charge[j]
                if ( charge_first*charge_second == -1 ) :
                    print( muon_charge[i], i,muon_charge[j], j)
                    zcandMass.append((muon_tlorentz[i]+muon_tlorentz[j]).M())


        for i in range(len(elec_charge)-1):
            charge_first = elec_charge[i]
            for j in range(len(elec_charge))[i+1:]:
                charge_second = elec_charge[j]
                if ( charge_first*charge_second == -1 ) :
                    print( elec_charge[i], i,elec_charge[j], j)
                    zcandMass.append((elec_tlorentz[i]+elec_tlorentz[j]).M())
    inROOTFile.Close()
    outFile = ROOT.TFile("zcandmass.root","RECREATE")
    h1 = ROOT.TH1F("zmass","zmass",100,0,100)
    for zmass in zcandMass:
        h1.Fill(zmass)
    h1.Write()
    outFile.Close()




if __name__ == "__main__":
    return_code = getZMass(sys.argv)
    sys.exit(return_code)

