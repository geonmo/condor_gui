#!/usr/bin/env python
import xml.etree.ElementTree as ET
import XRootD
from XRootD import client
from XRootD.client.flags import DirListFlags, OpenFlags, MkDirFlags, QueryCode
import socket
import glob

class SingletonInstance:
    __instance = None
    @classmethod
    def __getInstance(cls):
        return cls.__instance
    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance= cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class SearchROOT(SingletonInstance):
    info   = {}
    mapped = {}
    verbose = False
    everyChecking = False
    LFNPath= ""
    def __init__(self, sitename="local"):
        self.givenName = sitename
        self.loadSiteInfo(sitename)
    def fromLFN(self, LFN):
        self.LFNPath = self.validateLFN(LFN)
        if not self.LFNPath in self.mapped:
            self.mapped[self.LFNPath] = {}
        self.mapped[self.LFNPath]['PFNPath'] = ""
        self.mapped[self.LFNPath]['pfnChecked'] = False
        return self
    def validateLFN(self, LFN):
        if( LFN.startswith('/store')):
            return LFN
        else:
            location = LFN.find("/store")
            return LFN[location:]
    def changeSite(self, sitename):
        self.giveName = sitename
    def loadSiteInfo(self, sitename ):
        if( self.verbose ) :
            print("*"*50)
            print("Now, loading the site information about %s."%(sitename))
            print("*"*50)
        if (not sitename in self.info):
            self.info[sitename]= {}
            self.info[sitename]['protocols'] = []
            self.info[sitename]['urls'] = set()
        else:
            if (self.verbose):
                print("Already site info was loaded for same site. Skip the loading.")
        infomap = self.info[sitename]
        #### Acquire available protocols from SITECONF/local information 
        root = ET.parse("/cvmfs/cms.cern.ch/SITECONF/%s/JobConfig/site-local-config.xml"%(sitename)).getroot()
        sitesection = root.find("site")
        infomap['sitename_description'] = sitesection.attrib['name']
        evt_data = sitesection.find("event-data")
        for category in evt_data:
            protocol = category.attrib['url'].split("protocol")[-1].replace("=",'')
            #### Protocol Selection. srm, gsiftp, direct will be dropped.
            if ("srm" in protocol): continue
            if ("gsiftp" in protocol): continue
            if ("direct" in protocol): continue
            #### fallback pattern also will be dropped.
            if ("fallback" in protocol): continue
            infomap['protocols'].append(protocol)
        #### Acquire URL path using protocol  
        root = ET.parse('/cvmfs/cms.cern.ch/SITECONF/%s/PhEDEx/storage.xml'%(sitename)).getroot()
        tags = root.findall("lfn-to-pfn")
        for tag in tags:
            if tag.attrib['path-match'] != "/+store/(.*)" : continue
            if tag.attrib['protocol'] in infomap['protocols']:
                infomap['urls'].add( tag.attrib['result'] )
        infomap['updated'] = True
    def accessChecking(self):
        ## Skipped the access checking if pfn address is existed.
        if self.mapped[self.LFNPath]['pfnChecked']:
            if( self.verbose): 
                print("This LFN is already checked. Skipped.")
            return
        ## If preferredURL is set, skip the checking routine.
        if ('preferredURL' in self.info) and (not self.everyChecking):
            if(self.verbose):
                print("Preferred URL path is already set. Use this preferred url.")
            preferredPFN = self.info['preferredURL'].replace("/store/$1",self.LFNPath)
            self.mapped[self.LFNPath]['pfnChecked'] = True
            self.mapped[self.LFNPath]['PFNPath'] = preferredPFN
            return
        ## First, check the PFN using givenName.
        if (self.verbose) : 
            print("Checking the file on %s"%(self.givenName))
        if self.checkURL(self.givenName) : return
            
        ## Second, to use neighbor sites.
        print("[Warning] Failed to find the file at [%s]"%(self.givenName))
        country_code = self.getContryCode()
        site_list = glob.glob("/cvmfs/cms.cern.ch/SITECONF/*%s*"%(country_code))
        if ( self.verbose) : 
            print("Will find the file at neighbor sites.")
            print("Sites : %s"%site_list)
        for site_path in site_list:
            tier_site = site_path.split("/")[-1]
            self.loadSiteInfo(tier_site)
            if self.checkURL(tier_site) :
                return
        ## If all failes, use global redirector.
        global_redirector = "root://cmsxrootd.fnal.gov//store/$1"
        globalPath = global_redirector.replace("/store/$1",self.LFNPath) 
        ## Global redirector can not be set as preferredURL.
        self.mapped[self.LFNPath]['pfnChecked'] = True
        self.mapped[self.LFNPath]['PFNPath'] = globalPath
        return
    def getContryCode(self):
        temp  = self.info["local"]['sitename_description'].split("_")[1]
        temp2 = socket.gethostname()[-2:]
        if (len(temp) ==2):
            return temp.upper()
        else :
            return temp2.upper()
    def checkURL(self, site):
        if ( self.verbose) : print("check URL %s"%(site))
        urls = list(self.info[site]['urls'])
        if ( site == "T3_KR_KNU"):
            urls.append("root://cluster142.knu.ac.kr:1094//store/$1")
        for url in urls:
            test_PFN = url.replace("/store/$1",self.LFNPath)

            ### Global Redirector will be dropped for Accessing.
            if "cmsxrootd.fnal.gov" in test_PFN: continue
            if "xrootd-cms.infn.it" in test_PFN: continue
            if "cms-xrd.global.cern.ch" in test_PFN: continue

            if ( self.verbose ): 
                print("Trying to using "+test_PFN)
            with client.File() as f:
                result =  f.open(test_PFN, OpenFlags.READ, XRootD.client.flags.AccessMode.NONE, 5 )[0]
                if result.ok : 
                    self.mapped[self.LFNPath]['pfnChecked'] = True
                    self.mapped[self.LFNPath]['accessChecked'] = True
                    self.mapped[self.LFNPath]['PFNPath'] = test_PFN
                    self.info['preferredURL'] = url 
                    print("Successfully find the file at [%s]"%site)
                    return result.ok
                
    def getSiteName(self):
        return ( self.info['sitename'] )
    def getUrls(self):
        return ( list(self.urls) )
    def clear(self):
        self.info = {}
    def reset(self):
        if 'preferredURL' in self.info:
            del self.info['preferredURL']
    def verboseOn(self):
        self.verbose = True
    def test(self, siteinfo="local"):
        print(self.LFNPath)
        test_PFN = list(self.info[self.givenName]['urls'])[0].replace("$1",self.LFNPath)
        print(test_PFN)
    def toPFN(self):
        if self.mapped[self.LFNPath]:
            self.accessChecking()
        return self.mapped[self.LFNPath]['PFNPath']
    def LFN(self):
        return self.LFNPath



if __name__ == "__main__":
    print( "Case1. target file is located at local.")
    lfn = "/store/user/geonmo/Ups1SMM_5p02TeV_TuneCP5_Embd_RECO_20190401/190402_035044/0000/HIN-HINPbPbAutumn18DRHIMix-00003_step2_995.root"
    test1 = SearchROOT()
    test1.verboseOn()
    print( test1.fromLFN(lfn).toPFN())
    



