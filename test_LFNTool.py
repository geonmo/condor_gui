#!/usr/bin/env python

from LFNTool import SearchROOT

if __name__ == "__main__":
    print( "Case1. target file is located at local.")
    lfn = "/store/user/geonmo/Ups1SMM_5p02TeV_TuneCP5_Embd_RECO_20190401/190402_035044/0000/HIN-HINPbPbAutumn18DRHIMix-00003_step2_995.root"
    test1 = SearchROOT()
    test1.verboseOn()
    print( test1.fromLFN(lfn).toPFN())
    
    print( "\n"*2)
    print( "Case2. target file is located at local, too. The new instance must use preferredURL for speed")
    lfn2 = "/store/user/geonmo/Ups1SMM_5p02TeV_TuneCP5_Embd_RECO_20190401/190402_035044/0000/HIN-HINPbPbAutumn18DRHIMix-00003_step2_991.root"
    test2 = SearchROOT()
    print( test2.fromLFN(lfn2).toPFN())

    print( "\n"*2)
    ## To reset is required for other sources.
    test1.reset()
    print("Case3. Non-existed file")
    lfn3 = "/store/user/geonmo/aaaaaa.root"
    ## Reuse the previous instance.
    print( test1.fromLFN(lfn3).toPFN())

    print( "\n"*2)
    print("Case4. Retry local files with no instance.")
    lfn4 = "/store/user/geonmo/Ups1SMM_5p02TeV_TuneCP5_Embd_RECO_20190401/190402_035044/0000/HIN-HINPbPbAutumn18DRHIMix-00003_step2_980.root"
    print( SearchROOT().fromLFN(lfn4).toPFN())

    print( "\n"*2)
    lfn5 = "/store/user/geonmo/Ups1SMM_5p02TeV_TuneCP5_Embd_RECO_20190401/190402_035044/0000/HIN-HINPbPbAutumn18DRHIMix-00003_step2_979.root"
    print( SearchROOT().fromLFN(lfn5).toPFN())
