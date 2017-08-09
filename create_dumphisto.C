{
    TH1F* h1 = new TH1F("h1","h1",5,0,5);
    for(int i=0 ; i< 5 ; i++) {
        h1->Fill(i+0.5,(i+1)*10+i);
    }
    h1->SaveAs("histo.root");
}
