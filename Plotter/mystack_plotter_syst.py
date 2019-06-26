#coded by pctiwari
import ROOT as rt
import math,os,sys
import CMS_lumi, tdrstyle
import array, sample_xsec,optparse
import datetime
import os.path
import array as array

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

parser.add_option("-d", "--data", dest="datasetname")
parser.add_option("-i", "--inputfiles",  dest="inputfiles")
parser.add_option("-s", "--sr", action="store_true", dest="plotSRs")
parser.add_option("-m", "--mu", action="store_true", dest="plotMuRegs")
parser.add_option("-e", "--ele", action="store_true", dest="plotEleRegs")
parser.add_option("-p", "--pho", action="store_true", dest="plotPhoRegs")
parser.add_option("-q", "--qcd", action="store_true", dest="plotQCDRegs")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")

(options, args) = parser.parse_args()

if options.plotSRs==None:
    makeSRplots = False
else:
    makeSRplots = options.plotSRs

if options.plotMuRegs==None:
    makeMuCRplots = False
else:
    makeMuCRplots = options.plotMuRegs

if options.plotEleRegs==None:
    makeEleCRplots = False
else:
    makeEleCRplots = options.plotEleRegs

if options.plotPhoRegs==None:
    makePhoCRplots = False
else:
    makePhoCRplots = options.plotPhoRegs

if options.plotQCDRegs==None:
    makeQCDCRplots = False
else:
    makeQCDCRplots = options.plotQCDRegs

if options.verbose==None:
    verbose = False
else:
    verbose = options.verbose

if options.datasetname.upper()=="SE":
    dtset="SE"
elif options.datasetname.upper()=="SP":
    dtset="SP"
elif options.datasetname.upper()=="SM":
    dtset="SM"
else:
    dtset="MET"

print ("Using dataset "+dtset)

datestr = str(datetime.date.today().strftime("%d%m%Y"))

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = " Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 1800
W_ref = 2100
W = W_ref
H = H_ref

iPeriod = 4

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

canvas = rt.TCanvas("canvas","newcanvas",0,0,W,H); canvas.Draw()
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

hists=[]
regions=[]
PUreg=[]
lumi2016 = 35.9 * 1000

os.system("ls "+options.inputfiles+" | cat > samplelist.txt")

def makeplot(plot_location,plot,titleX,XMIN,XMAX,Rebin,ISLOG,NORATIOPLOT,reg,blindfactor=1.):
    file=open("samplelist.txt","r")
    xsec=1.0
    norm = 1.0
    BLINDFACTOR = 1.0
    r_fold = 'rootFiles/'
    DIBOSON = rt.TH1F()
    Top = rt.TH1F()
    WJets = rt.TH1F()
    DYJets = rt.TH1F()
    ZJets = rt.TH1F()
    STop = rt.TH1F()
    GJets = rt.TH1F()
    QCD = rt.TH1F()
    DYJets_files  = []; ZJets_files = []
    WJets_files   = []; GJets_files = []
    DIBOSON_files = []; STop_files  = []
    Top_files     = []; QCD_files   = []
    data_file_MET = []; data_file_SE = []
    for i in file.readlines()[:]:
        f = rt.TFile(options.inputfiles+'/'+str(i.rstrip()),'READ')
        file_name = str(f)
        if 'data_combined_MET' in file_name:
            data_file_MET.append(f)
        elif 'data_combined_SE' in file_name:
            data_file_SE.append(f)
        elif 'DYJetsToLL_M-50' in file_name:
            DYJets_files.append(f)
        elif 'ZJetsToNuNu' in file_name:
            ZJets_files.append(f)
        elif 'WJetsToLNu_HT' in file_name:
            WJets_files.append(f)
        elif 'GJets_HT' in file_name:
            GJets_files.append(f)
        elif 'QCD' in file_name:
            QCD_files.append(f)
        #elif 'TT_T' or 'TTT' in file_name:
        elif 'TT_T' in file_name:
            Top_files.append(f)
        elif ('WWTo' in file_name) or ('WZTo' in file_name) or ('ZZTo' in file_name):
            DIBOSON_files.append(f)
        elif ('ST_t' in file_name) or ('ST_s' in file_name):
            STop_files.append(f)

    plot_hadrecoil = 'hadrecoil' in str(plot)
    plot_varBin=False

    if plot_hadrecoil:
        plot_varBin = True
        bins=[200,250,350,500,1000]

    for inum in range(len(DYJets_files)):
        xsec = sample_xsec.getXsec(str(DYJets_files[inum]))
        hist_integral = DYJets_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            DYJets = (DYJets_files[inum].Get(str(plot)))
            DYJets.Scale(norm)
            if plot_varBin:
                DYJets=DYJets.Rebin(len(bins)-1,"DYJets",array.array('d',bins))
                DYJets.SetBinContent(len(bins)-1,DYJets.GetBinContent(len(bins)-1)+DYJets.GetBinContent(len(bins)))
                DYJets.SetBinContent(len(bins),0.)
            else:
                DYJets=DYJets.Rebin(Rebin)
        else:
            temp_hist = DYJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            DYJets.Add(temp_hist)
    DYJets.Sumw2()

    for inum in range(len(GJets_files)):
        xsec = sample_xsec.getXsec(str(GJets_files[inum]))
        #print('Gjet xsec: ', xsec)
        hist_integral = GJets_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            GJets = (GJets_files[inum].Get(str(plot)))
            GJets.Scale(norm)
            if plot_varBin:
                GJets=GJets.Rebin(len(bins)-1,"GJets",array.array('d',bins))
                GJets.SetBinContent(len(bins)-1,GJets.GetBinContent(len(bins)-1)+GJets.GetBinContent(len(bins)))
                GJets.SetBinContent(len(bins),0.)
            else:
                GJets=GJets.Rebin(Rebin)
        else:
            temp_hist = GJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            GJets.Add(temp_hist)
    GJets.Sumw2()

    for inum in range(len(ZJets_files)):
        xsec = sample_xsec.getXsec(str(ZJets_files[inum]))
        #print('Zjet xsec: ', xsec)
        hist_integral = ZJets_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            ZJets = (ZJets_files[inum].Get(str(plot)))
            ZJets.Scale(norm)
            if plot_varBin:
                ZJets=ZJets.Rebin(len(bins)-1,"ZJets",array.array('d',bins))
                ZJets.SetBinContent(len(bins)-1,ZJets.GetBinContent(len(bins)-1)+ZJets.GetBinContent(len(bins)))
                ZJets.SetBinContent(len(bins),0.)
            else:
                ZJets=ZJets.Rebin(Rebin)
        else:
            temp_hist = ZJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            ZJets.Add(temp_hist)
    ZJets.Sumw2()
    for inum in range(len(WJets_files)):
        xsec = sample_xsec.getXsec(str(WJets_files[inum]))
        #print('Wjet xsec: ', xsec)
        hist_integral = WJets_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            WJets = (WJets_files[inum].Get(str(plot)))
            WJets.Scale(norm)
            if plot_varBin:
                WJets=WJets.Rebin(len(bins)-1,"WJets",array.array('d',bins))
                WJets.SetBinContent(len(bins)-1,WJets.GetBinContent(len(bins)-1)+WJets.GetBinContent(len(bins)))
                WJets.SetBinContent(len(bins),0.)
            else:
                WJets=WJets.Rebin(Rebin)
        else:
            temp_hist = WJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            WJets.Add(temp_hist)
    WJets.Sumw2()

    for inum in range(len(DIBOSON_files)):
        xsec = sample_xsec.getXsec(str(DIBOSON_files[inum]))
        hist_integral = DIBOSON_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            DIBOSON = (DIBOSON_files[inum].Get(str(plot)))
            DIBOSON.Scale(norm)
            if plot_varBin:
                DIBOSON=DIBOSON.Rebin(len(bins)-1,"DIBOSON",array.array('d',bins))
                DIBOSON.SetBinContent(len(bins)-1,DIBOSON.GetBinContent(len(bins)-1)+DIBOSON.GetBinContent(len(bins)))
                DIBOSON.SetBinContent(len(bins),0.)
            else:
                DIBOSON=DIBOSON.Rebin(Rebin)
        else:
            temp_hist = DIBOSON_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)

            DIBOSON.Add(temp_hist)
    DIBOSON.Sumw2()

    for inum in range(len(Top_files)):
        xsec = sample_xsec.getXsec(str(Top_files[inum]))
        hist_integral = Top_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            Top = (Top_files[inum].Get(str(plot)))
            Top.Scale(norm)
            if plot_varBin:
                Top=Top.Rebin(len(bins)-1,"Top",array.array('d',bins))
                Top.SetBinContent(len(bins)-1,Top.GetBinContent(len(bins)-1)+Top.GetBinContent(len(bins)))
                Top.SetBinContent(len(bins),0.)
            else:
                Top=Top.Rebin(Rebin)
        else:
            temp_hist = Top_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            Top.Add(temp_hist)
    Top.Sumw2()

    for inum in range(len(STop_files)):
        xsec = sample_xsec.getXsec(str(STop_files[inum]))
        #print('STop xsec: ', xsec)
        hist_integral = STop_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            STop = (STop_files[inum].Get(str(plot)))
            STop.Scale(norm)
            if plot_varBin:
                STop=STop.Rebin(len(bins)-1,"STop",array.array('d',bins))
                STop.SetBinContent(len(bins)-1,STop.GetBinContent(len(bins)-1)+STop.GetBinContent(len(bins)))
                STop.SetBinContent(len(bins),0.)
            else:
                STop=STop.Rebin(Rebin)
        else:
            temp_hist = STop_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            STop.Add(temp_hist)
    STop.Sumw2()

    for inum in range(len(QCD_files)):
        xsec = sample_xsec.getXsec(str(QCD_files[inum]))
        #print('QCD xsec: ', xsec)
        hist_integral = QCD_files[inum].Get('h_total_weight').Integral()
        norm = (lumi2016*xsec)/(hist_integral*blindfactor)
        if inum==0:
            QCD = (QCD_files[inum].Get(str(plot)))
            QCD.Scale(norm)
            if plot_varBin:
                QCD=QCD.Rebin(len(bins)-1,"QCD",array.array('d',bins))
                QCD.SetBinContent(len(bins)-1,QCD.GetBinContent(len(bins)-1)+QCD.GetBinContent(len(bins)))
                QCD.SetBinContent(len(bins),0.)
            else:
                QCD=QCD.Rebin(Rebin)
        else:
            temp_hist = QCD_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_varBin:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            else:
                temp_hist=temp_hist.Rebin(Rebin)
            QCD.Add(temp_hist)
    QCD.Sumw2()

    ZJetsCount = ZJets.Integral()
    DYJetsCount = DYJets.Integral()
    WJetsCount = WJets.Integral()
    STopCount = STop.Integral()
    GJetsCount = GJets.Integral()
    TopCount = Top.Integral()
    VVCount = DIBOSON.Integral()
    QCDCount = QCD.Integral()

    mcsum = ZJetsCount + DYJetsCount + WJetsCount + STopCount + GJetsCount + TopCount + VVCount +  QCDCount
    total_MC = DYJets_files + ZJets_files + WJets_files + GJets_files + Top_files + DIBOSON_files + STop_files + QCD_files

    hs = rt.THStack("hs", " ")
    #Colors for Histos
    DYJets.SetFillColor(rt.kGreen + 2)
    DYJets.SetLineWidth(0)

    ZJets.SetFillColor(rt.kAzure + 1)
    ZJets.SetLineWidth(0)

    DIBOSON.SetFillColor(rt.kBlue + 2)
    DIBOSON.SetLineWidth(0)

    Top.SetFillColor(rt.kOrange - 2)
    Top.SetLineWidth(0)

    WJets.SetFillColor(rt.kViolet - 3)
    WJets.SetLineWidth(0)

    STop.SetFillColor(rt.kOrange + 1)
    STop.SetLineWidth(0)

    GJets.SetFillColor(rt.kCyan - 9)
    GJets.SetLineWidth(0)

    QCD.SetFillColor(rt.kGray + 1)
    QCD.SetLineWidth(0)

    #add the histos to THStack
    hs.Add(QCD, "hist")
    hs.Add(GJets, "hist")
    hs.Add(DYJets, "hist")
    hs.Add(DIBOSON, "hist")
    hs.Add(STop, "hist")
    hs.Add(WJets, "hist")
    hs.Add(Top, "hist")
    hs.Add(ZJets, "hist")

    if makeMuCRplots or makeSRplots:
        data_obs = data_file_MET[0].Get(str(plot))
    elif makeEleCRplots:
        data_obs = data_file_SE[0].Get(str(plot))
    if plot_varBin:
        data_obs=data_obs.Rebin(len(bins)-1,"data_obs",array.array('d',bins))
        data_obs.SetBinContent(len(bins)-1,data_obs.GetBinContent(len(bins)-1)+data_obs.GetBinContent(len(bins)))
        data_obs.SetBinContent(len(bins),0.)
    data_obs.SetMarkerColor(rt.kBlack)
    data_obs.SetMarkerStyle(20)

    Stackhist = hs.GetStack().Last()
    maxi = Stackhist.GetMaximum()
    Stackhist.SetLineWidth(0)

    if (NORATIOPLOT):
        canvas1_1 = rt.TPad("canvas1_1", "newpad", 0, 0.05, 1, 1); canvas1_1.Draw()
    else:
        canvas1_1 = rt.TPad("canvas1_1", "newpad", 0, 0.28, 1, 1); canvas1_1.Draw()

    canvas1_1.SetLeftMargin( L/W )
    canvas1_1.SetRightMargin( R/W )
    canvas1_1.SetBottomMargin(0.03)
    canvas1_1.SetTopMargin( (T/H)*1.2 )
    canvas1_1.SetLogy(ISLOG)
    canvas1_1.Draw()
    canvas1_1.cd()
    hs.Draw()
    if not plot_varBin:hs.GetXaxis().SetRangeUser(XMIN, XMAX)
    hs.GetXaxis().SetTitle('Events')
    if (ISLOG):
        hs.SetMaximum(maxi * 50)
        hs.SetMinimum(1)
    else:
        hs.SetMaximum(maxi * 1.35)
        hs.SetMinimum(0)

    hs.GetXaxis().SetTickLength(0.04);
    #hs.GetXaxis().SetNdivisions(508);
    if (NORATIOPLOT):
        hs.GetYaxis().SetTitle("Events")
        hs.GetYaxis().SetTitleSize(0.05)
        hs.GetYaxis().SetTitleFont(42)
        hs.GetYaxis().SetLabelFont(42)
        hs.GetYaxis().SetLabelSize(.03)
        #hs.GetYaxis().SetMoreLogLabels()
    else:
        hs.GetYaxis().SetTitle("Events")
        hs.GetYaxis().SetTitleSize(0.045)
        hs.GetYaxis().SetTitleOffset(0.8)
        hs.GetYaxis().SetTitleFont(42)
        hs.GetYaxis().SetLabelFont(42);
        hs.GetYaxis().SetLabelSize(.03)
        #hs.GetYaxis().SetMoreLogLabels();


    data_obs.SetLineColor(rt.kBlack)
    data_obs.SetFillColor(rt.kBlack)
    data_obs.SetMarkerSize(2)
    data_obs.SetLineWidth(1)
    data_obs.Rebin(Rebin)
    if not NORATIOPLOT:
        data_obs.Draw("same p e1")

    #set the colors and size for the legend
    latex = rt.TLatex()
    n_ = 2

    x1_l = 0.92
    y1_l = 0.90

    dx_l = 0.25
    dy_l = 0.40
    x0_l = x1_l-dx_l
    y0_l = y1_l-dy_l

    legend = rt.TLegend(x0_l,y0_l,x1_l, y1_l,"", "brNDC")
    legend.SetNColumns(2)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    #legend =  rt.("legend_0","legend_0",x0_l,y0_l,x1_l, y1_l )
    legend.AddEntry(data_obs, "Data", "PEL")
    legend.AddEntry(ZJets, "Z(#nu#nu) + jets", "f")
    legend.AddEntry(Top, "Top", "f")
    legend.AddEntry(WJets, "W(l#nu) + jets", "f")
    legend.AddEntry(STop, "Single t", "f")
    legend.AddEntry(DIBOSON, "VV, VH", "f")
    legend.AddEntry(DYJets, "Z(ll) + jets", "f")
    legend.AddEntry(GJets, "G jets", "f")
    legend.AddEntry(QCD, "Multijet", "f")
    legend.Draw('same')

    #error
    h_err = rt.TH1F()
    h_temp_ = total_MC[0].Get(str(plot))
    if plot_varBin:
	h_temp_=h_temp_.Rebin(len(bins)-1,"h_temp1_",array.array('d',bins))
        h_temp_.SetBinContent(len(bins)-1,h_temp_.GetBinContent(len(bins)-1)+h_temp_.GetBinContent(len(bins)))
        h_temp_.SetBinContent(len(bins),0.)
    h_err = h_temp_.Clone("h_err")
    h_err.Sumw2()
    h_err.Reset()
    for i in range(len(total_MC)):
        if i==0: continue
        h_temp1_ = total_MC[i].Get(str(plot))
        if plot_varBin:
	    h_temp1_=h_temp1_.Rebin(len(bins)-1,"h_temp1_",array.array('d',bins))
            h_temp1_.SetBinContent(len(bins)-1,h_temp1_.GetBinContent(len(bins)-1)+h_temp1_.GetBinContent(len(bins)))
            h_temp1_.SetBinContent(len(bins),0.)
        h_err.Add(h_temp1_)
    h_err.Sumw2()
    h_err.SetFillColor(rt.kGray+3)
    h_err.SetLineColor(rt.kGray+3)
    h_err.SetMarkerSize(0)
    h_err.SetFillStyle(3013)
    h_err.Draw("E2 SAME")

    ratiostaterr = h_err.Clone("ratiostaterr")
    ratiostaterr.Sumw2()
    ratiostaterr.SetStats(0)
    ratiostaterr.SetMinimum(0)
    ratiostaterr.SetMarkerSize(0)
    ratiostaterr.SetFillColor(rt.kBlack)
    ratiostaterr.SetFillStyle(3013)

    for i in range(0,h_err.GetNbinsX()+2):
        ratiostaterr.SetBinContent(i, 1.0)
        if (h_err.GetBinContent(i) > 1e-6):
            binerror = h_err.GetBinError(i)/h_err.GetBinContent(i)
            ratiostaterr.SetBinError(i, binerror)
        else:
            ratiostaterr.SetBinError(i, 999.)

    ratiosysterr = ratiostaterr.Clone("ratiosysterr")
    ratiosysterr.Sumw2()
    ratiosysterr.SetMarkerSize(0)
    ratiosysterr.SetFillColor(rt.kGray)
    ratiosysterr.SetFillStyle(1001)

    for i in range(0,h_err.GetNbinsX()+2):
        if (h_err.GetBinContent(i) > 1e-6):
            binerror2 = (pow(h_err.GetBinError(i), 2) +
                pow(0.25 * WJets.GetBinContent(i), 2) +
                pow(0.25 * ZJets.GetBinContent(i), 2) +
                pow(0.20 * DYJets.GetBinContent(i), 2) +
                pow(0.25 * Top.GetBinContent(i), 2) +
                pow(0.20 * GJets.GetBinContent(i), 2) +
                pow(0.20 * QCD.GetBinContent(i), 2) +
                pow(0.25 * STop.GetBinContent(i), 2) +
                pow(0.20 * DIBOSON.GetBinContent(i), 2))
            binerror = math.sqrt(binerror2)
            ratiosysterr.SetBinError(i, binerror/h_err.GetBinContent(i))

    ratioleg = rt.TLegend(0.6, 0.88, 0.89, 0.98)
    ratioleg.SetLineColor(0)
    ratioleg.SetShadowColor(0)
    ratioleg.SetTextFont(42)
    ratioleg.SetTextSize(0.09)
    ratioleg.SetBorderSize(1)
    ratioleg.SetNColumns(2)
    #ratioleg.AddEntry(ratiosysterr, "stat + syst", "f")
    ratioleg.AddEntry(ratiostaterr, "stat", "f")

    #For DATA:
    if not NORATIOPLOT:
        canvas.cd()
        #DataMC = rt.TH1F()
        DataMC = data_obs.Clone("DataMC")
        #DataMC.Add(Stackhist,-1) ##for (data-MC)/MC
        DataMCPre = data_obs.Clone("DataMCPre")
        DataMC.Divide(Stackhist)
        #DataMCPre->Divide(h_prefit)
        DataMC.GetYaxis().SetTitle("Data/Pred.")
        #DataMC.GetYaxis().SetTitle("#frac{Data-Pred}{Pred.}")
        DataMC.GetYaxis().SetTitleSize(0.1)
        DataMC.GetYaxis().SetTitleOffset(0.42)
        DataMC.GetYaxis().SetTitleFont(42)
        DataMC.GetYaxis().SetLabelSize(0.08)
        DataMC.GetYaxis().CenterTitle()
        DataMC.GetXaxis().SetTitle(titleX)
        DataMC.GetXaxis().SetLabelSize(0.1)
        DataMC.GetXaxis().SetTitleSize(0.1)
        DataMC.GetXaxis().SetTitleOffset(1)
        DataMC.GetXaxis().SetTitleFont(42)
        DataMC.GetXaxis().SetTickLength(0.04)
        DataMC.GetXaxis().SetLabelFont(42)
        DataMC.GetYaxis().SetLabelFont(42)

    canvas1_2 = rt.TPad("canvas1_2", "newpad", 0, 0.00, 1, 0.3); canvas1_2.Draw()
    if not NORATIOPLOT: canvas1_2.Draw()
    canvas1_2.cd()
    canvas1_2.Range(-7.862408, -629.6193, 53.07125, 486.5489)
    canvas1_2.SetFillColor(0)
    canvas1_2.SetTicky(1)
    canvas1_2.SetLeftMargin( L/W )
    canvas1_2.SetRightMargin( R/W )
    canvas1_2.SetTopMargin(0.00)
    canvas1_2.SetBottomMargin((B/H)*2.5)
    canvas1_2.SetFrameFillStyle(0)
    canvas1_2.SetFrameBorderMode(0)
    canvas1_2.SetFrameFillStyle(0)
    canvas1_2.SetFrameBorderMode(0)
    canvas1_2.SetLogy(0)

    if not NORATIOPLOT:
        if not plot_varBin:DataMC.GetXaxis().SetRangeUser(XMIN, XMAX)
        DataMC.SetMarkerSize(2)
        DataMC.SetMarkerStyle(20)
        DataMC.SetMarkerColor(1)
        #DataMCPre.SetMarkerSize(0.7)
        #DataMCPre.SetMarkerStyle(20)
        #DataMCPre.SetMarkerColor(rt.kRed)
        #DataMCPre.SetLineColor(rt.kRed)
        DataMC.Draw("P e1")
        ratiostaterr.Draw("e2 same")
        DataMC.Draw("P e1 same")
        DataMC.SetMinimum(-0.2)
        DataMC.SetMaximum(2.1)
        DataMC.GetXaxis().SetNdivisions(508)
        DataMC.GetYaxis().SetNdivisions(505)
        line0 = rt.TLine(XMIN, 1, XMAX, 1)
        line0.SetLineStyle(3)
        line0.Draw("same")
        canvas1_2.SetGridy()
        ratioleg.Draw("same")
        canvas1_2.Update()
        canvas1_2.Draw()
    #draw the CR text on the canvas
    canvas.cd()
    crname_latex = rt.TLatex(0.26, 0.8, reg +' CR')
    crname_latex.SetNDC()
    crname_latex.SetTextAngle(0)
    crname_latex.SetTextColor(rt.kBlack)
    crname_latex.Draw("same")

    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()
    canvas.Update()
    canvas.Draw()

    if not os.path.exists('plots/'+datestr+'syst/bbDMPng/'+reg):
        os.makedirs('plots/'+datestr+'syst/bbDMPng/'+reg)
    if not os.path.exists('plots/'+datestr+'syst/bbDMPdf/'+reg):
        os.makedirs('plots/'+datestr+'syst/bbDMPdf/'+reg)
    if not os.path.exists('plots/'+datestr+'syst/bbDMRoot/'+reg):
        os.makedirs('plots/'+datestr+'syst/bbDMRoot/'+reg)
    if (ISLOG == 0):
        canvas.SaveAs('plots/'+datestr+'syst/bbDMPdf/'+reg+'/'+plot+'.pdf')
        canvas.SaveAs('plots/'+datestr+'syst/bbDMPng/'+reg+'/'+plot+'.png')
        print("Saved. \n")
    if (ISLOG == 1):
        canvas.SaveAs('plots/'+datestr+'syst/bbDMPdf/'+reg+'/'+plot+'_log.pdf')
        canvas.SaveAs('plots/'+datestr+'syst/bbDMPng/'+reg+'/'+plot+'_log.png')
        print("Saved. \n")

    fshape = rt.TFile('plots/'+datestr+'syst/bbDMRoot/'+reg+'/'+plot+'.root', "RECREATE");
    fshape.cd();
    #Save root files for datacards
    Stackhist.SetNameTitle("bkgSum", "bkgSum");
    Stackhist.Write();
    DIBOSON.SetNameTitle("DIBOSON", "DIBOSON");
    DIBOSON.Write();
    ZJets.SetNameTitle("ZJets", "ZJets");
    ZJets.Write();
    GJets.SetNameTitle("GJets", "GJets");
    GJets.Write();
    QCD.SetNameTitle("QCD", "QCD");
    QCD.Write();
    STop.SetNameTitle("STop", "STop");
    STop.Write();
    Top.SetNameTitle("TT", "Top");
    Top.Write();
    WJets.SetNameTitle("WJets", "WJets");
    WJets.Write();
    DYJets.SetNameTitle("DYJets", "DYJets");
    DYJets.Write();
    data_obs.SetNameTitle("data_obs", "data_obs");
    data_obs.Write();
    fshape.Write();
    fshape.Close();
    #update the canvas to draw the legend


# In[4]:


dirnames=['']

srblindfactor='1'
srnodata='1'

for dirname in dirnames:

    regions=[]
    PUreg=[]

    if makeMuCRplots:
        regions+=['1mutop1b','1mutop2b','2mu1b','2mu2b','1mu1b','1mu2b']
        PUreg+=['mu_']
    if makeEleCRplots:
        regions+=['1etop1b','1etop2b','2e1b','2e2b','1e1b','1e2b']
        PUreg+=['ele_']
    if makePhoCRplots:
        regions+=['1gamma1b','1gamma2b']
        PUreg+=['pho_']
    if makeQCDCRplots:
        regions+=['QCD1b','QCD2b']
        PUreg

    if makeSRplots:
        makeplot(dirname+"reg_sr1_hadrecoil",'h_met_sr1_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_btag_syst_up",'h_btag_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_btag_syst_down",'h_btag_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_lep_syst_up",'h_lep_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_lep_syst_down",'h_lep_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_met_syst_up",'h_metTrig_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_met_syst_down",'h_metTrig_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_jec_syst_up",'h_jec_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_jec_syst_down",'h_jec_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_jer_syst_up",'h_jer_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_jer_syst_down",'h_jer_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_pho_syst_up",'h_pho_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_pho_syst_down",'h_pho_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr1_ewkZ_syst_up",'h_ewkZ_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_ewkZ_syst_down",'h_ewkZ_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_ewkW_syst_up",'h_ewkW_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_ewkW_syst_down",'h_ewkW_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_ewkTop_syst_up",'h_ewkTop_syst_sr1_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr1_ewkTop_syst_down",'h_ewkTop_syst_sr1_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)

        makeplot(dirname+"reg_sr2_hadrecoil",'h_met_sr2_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_btag_syst_up",'h_btag_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_btag_syst_down",'h_btag_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_lep_syst_up",'h_lep_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_lep_syst_down",'h_lep_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_met_syst_up",'h_metTrig_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_met_syst_down",'h_metTrig_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_jec_syst_up",'h_jec_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_jec_syst_down",'h_jec_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_jer_syst_up",'h_jer_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_jer_syst_down",'h_jer_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_pho_syst_up",'h_pho_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_pho_syst_down",'h_pho_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

        makeplot(dirname+"reg_sr2_ewkZ_syst_up",'h_ewkZ_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_ewkZ_syst_down",'h_ewkZ_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_ewkW_syst_up",'h_ewkW_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_ewkW_syst_down",'h_ewkW_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_ewkTop_syst_up",'h_ewkTop_syst_sr2_up_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)
        makeplot(dirname+"reg_sr2_ewkTop_syst_down",'h_ewkTop_syst_sr2_down_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

    for reg in regions:
        try:
            makeplot(dirname+"reg_"+reg+"_hadrecoil",'h_reg_'+reg+'_hadrecoil_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_btag_syst_up",'h_btag_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_btag_syst_down",'h_btag_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_lep_syst_up",'h_lep_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_lep_syst_down",'h_lep_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)

            makeplot(dirname+"reg_"+reg+"_met_syst_up",'h_metTrig_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_met_syst_down",'h_metTrig_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)

            makeplot(dirname+"reg_"+reg+"_jer_syst_up",'h_jer_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_jer_syst_down",'h_jer_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)

            makeplot(dirname+"reg_"+reg+"_jec_syst_up",'h_jec_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_jec_syst_down",'h_jec_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)

            makeplot(dirname+"reg_"+reg+"_ewkZ_syst_up",'h_ewkZ_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_ewkZ_syst_down",'h_ewkZ_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_ewkW_syst_up",'h_ewkW_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_ewkW_syst_down",'h_ewkW_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_ewkTop_syst_up",'h_ewkTop_syst_'+reg+'_up_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_ewkTop_syst_down",'h_ewkTop_syst_'+reg+'_down_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
        except Exception as e:
            print (e)
            print ("Cannot Plot")
            pass
