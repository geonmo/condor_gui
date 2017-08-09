void run(const char* infile)
{
    TFile* file = TFile::Open(infile);
    TH1F* h1 = (TH1F*)file->Get("h1");
    std::cout<<h1->GetBinContent(2)<<std::endl;
}
