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

def setHistStyle(h_temp2, hists, varbin):
    h_temp_ = h_temp2
    if 'Recoil' in hist or 'MET' in hist
        bins=[200,250,350,500,1000]
    if varbin:
        h_temp_=h_temp2.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
        h_temp_.SetBinContent(len(bins)-1,h_temp_.GetBinContent(len(bins)-1)+h_temp_.GetBinContent(len(bins))) #Add overflow bin content to last bin
        h_temp_.SetBinContent(len(bins),0.)
    else:
        h_temp_=h_temp2
    return h_temp_

def makeplot(plot_location,plot,titleX,XMIN,XMAX,Rebin,ISLOG,NORATIOPLOT,reg,blindfactor=1.):
    files=open("samplelist.txt","r")
    xsec=1.0;  norm = 1.0
    BLINDFACTOR = 1.0
    r_fold = 'rootFiles/'
    if Rebin==1:
        isrebin = True
    else:
        isrebin = False
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
    for file in files.readlines()[:]:
        myFile=path+'/'+file.rstrip()
        print ('running for file',myFile)
        print ('histName',hist)
        Str=str(count)
        exec("f"+Str+"=ROOT.TFile(myFile,'READ')",locals(), globals())
        exec("h_temp=f"+Str+".Get("+"\'"+str(hist)+"\'"+")",locals(), globals())
        exec("h_total_weight=f"+Str+".Get('h_total_mcweight')",locals(), globals())
        total_events = h_total_weight.Integral()
        print ('selected events',h_temp.Integral())

        if 'data_combined_MET' in file:
            h_temp=setHistStyle(h_temp, hist,isrebin)
            data_file_MET.append(h_temp)
        elif 'data_combined_SE' in file:
            h_temp=setHistStyle(h_temp, hist,isrebin)
            data_file_SE.append(h_temp)

        elif 'DYJetsToLL_M-50' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            DYJets_files.append(h_temp)

        elif 'ZJetsToNuNu' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            ZJets_files.append(h_temp)
        elif 'WJetsToLNu_HT' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            WJets_files.append(h_temp)
        elif 'GJets_HT' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            GJets_files.append(h_temp)
        elif 'QCD' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            QCD_files.append(h_temp)
        #elif 'TT_T' or 'TTT' in file:
        elif 'TTT' in file:
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            Top_files.append(h_temp)
        elif ('WWTo' in file) or ('WZTo' in file) or ('ZZTo' in file):
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            DIBOSON_files.append(h_temp)
        elif ('ST_t' in file) or ('ST_s' in file):
            xsec = sample_xsec.getXsec(file)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            h_temp=setHistStyle(h_temp, hist,isrebin)
            STop_files.append(h_temp)
    ###==========================================================add all the histograms regional based ======================================
    for i in range(len(WJets_files)):
        if i==0:
            WJets=WJets_files[i]
        else:WJets.Add(WJets_files[i])
    WJets.Sumw2()

    for i in range(len(DYJets_files)):
        if i==0:
            DYJets=DYJets_files[i]
        else:DYJets.Add(DYJets_files[i])
    DYJets.Sumw2()

    for i in range(len(ZJets_files)):
        if i==0:
            ZJets=ZJets_files[i]
        else:ZJets.Add(ZJets_files[i])
    ZJets.Sumw2()

    for i in range(len(GJets_files)):
        if i==0:
            GJets=GJets_files[i]
        else:GJets.Add(GJets_files[i])
    GJets.Sumw2()

    for i in range(len(DIBOSON_files)):
        if i==0:
            DIBOSON=DIBOSON_files[i]
        else:DIBOSON.Add(DIBOSON_files[i])
    DIBOSON.Sumw2()

    for i in range(len(STop_files)):
        if i==0:
            STop=STop_files[i]
        else:STop.Add(STop_files[i])
    STop.Sumw2()

    for i in range(len(Top_files)):
        if i==0:
            Top=Top_files[i]
        else:Top.Add(Top_files[i])
    Top.Sumw2()

    for i in range(len(QCD_files)):
        if i==0:
            QCD=QCD_files[i]
        else:QCD.Add(QCD_files[i])
    QCD.Sumw2()

    ##=================================================================

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

    if not os.path.exists('plots_norm/'+datestr+'/bbDMPng/'+reg):
        os.makedirs('plots_norm/'+datestr+'/bbDMPng/'+reg)
    if not os.path.exists('plots_norm/'+datestr+'/bbDMPdf/'+reg):
        os.makedirs('plots_norm/'+datestr+'/bbDMPdf/'+reg)
    if not os.path.exists('plots_norm/'+datestr+'/bbDMRoot/'+reg):
        os.makedirs('plots_norm/'+datestr+'/bbDMRoot/'+reg)
    if (ISLOG == 0):
        canvas.SaveAs('plots_norm/'+datestr+'/bbDMPdf/'+reg+'/'+plot+'.pdf')
        canvas.SaveAs('plots_norm/'+datestr+'/bbDMPng/'+reg+'/'+plot+'.png')
        print("Saved. \n")
    if (ISLOG == 1):
        canvas.SaveAs('plots_norm/'+datestr+'/bbDMPdf/'+reg+'/'+plot+'_log.pdf')
        canvas.SaveAs('plots_norm/'+datestr+'/bbDMPng/'+reg+'/'+plot+'_log.png')
        print("Saved. \n")

    fshape = rt.TFile('plots_norm/'+datestr+'/bbDMRoot/'+reg+'/'+plot+'.root', "RECREATE");
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
        regions+=['ZmumuCR_1b','ZmumuCR_2b','Wmunu_1b','Wmunu_2b','Topmunu_1b','Topmunu_2b']
        PUreg+=['mu_']
    if makeEleCRplots:
        regions+=['ZeeCR_1b','ZeeCR_2b','Wenu_1b','Wenu_2b','Topenu_1b','Topenu_2b']
        PUreg+=['ele_']
    if makePhoCRplots:
        regions+=['1gamma1b','1gamma2b']
        PUreg+=['pho_']
    if makeQCDCRplots:
        regions+=['QCD1b','QCD2b']
        PUreg

    makeplot(dirname+"CRSum",'h_CRSum_','',0.,10.,1,1,0,'cutflow')
    if makeMuCRplots: makeplot(dirname+"CRSumMu",'h_CRSumMu_','',0.,6.,1,1,0,'cutflow')
    if makeEleCRplots: makeplot(dirname+"CRSumEle",'h_CRSumEle_','',0.,4.,1,1,0,'cutflow')

    for dt in PUreg:
        makeplot(dirname+dt+"PuReweightPV",'h_'+dt+'PuReweightPV_','nPV after PU reweighting',0.,50.,1,0,0,'PUreweight')
        makeplot(dirname+dt+"noPuReweightPV",'h_'+dt+'noPuReweightPV_','nPV before PU reweighting',0.,50.,1,0,0,'PUreweight')
#        makeplot([dirname+dt+"PuReweightnPVert",'h_'+dt+'PuReweightnPVert_','nPV after PU reweighting (nPVert): '+dt,'0.','100.','100','0'])
#        makeplot([dirname+dt+"noPuReweightnPVert",'h_'+dt+'noPuReweightnPVert_','nPV before PU reweighting (nPVert): '+dt,'0.','100.','100','0'])

# Cutflow plots:
    # if makeSRplots:
    #     makeplot([dirname+"cutflow",'h_cutflow_','Cutflow','0.','10','1','1','1',srblindfactor,srnodata])
    #     makeplot([dirname+"cutflow_SR1",'h_cutflow_SR1_','SR1 Cutflow','0.','10','1','1','1',srblindfactor,srnodata])
    #     makeplot([dirname+"cutflow_SR2",'h_cutflow_SR2_','SR2 Cutflow','0.','10','1','1','1',srblindfactor,srnodata])
    if makeSRplots:
        makeplot(dirname+"reg_sr1_hadrecoil",'h_met_sr1_','Missing Transverse Energy',200.,1000.,1,1,0,'SR1',20)
        makeplot(dirname+"reg_sr2_hadrecoil",'h_met_sr2_','Missing Transverse Energy',200.,1000.,1,1,0,'SR2',20)

    for reg in regions:
        makeplot(dirname+"cutflow_"+reg,'h_cutflow_'+reg+'_',reg+' Cutflow',0.,13,1,1,0,reg)


    for reg in regions:
        try:
            if reg[0]=='2': makeplot(dirname+"reg_"+reg+"_ZpT",'h_reg_'+reg+'_ZpT_','Z candidate p_{T} (GeV)',0.,800.,reg[-2],1,0,reg)
            if reg[0]=='1': makeplot(dirname+"reg_"+reg+"_WpT",'h_reg_'+reg+'_WpT_','W candidate p_{T} (GeV)',200.,800.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_hadrecoil",'h_reg_'+reg+'_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_NHadEF",'h_reg_'+reg+'_jet1_NHadEF_','Lead jet neutral hadronic fraction',0.,1.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_CHadEF",'h_reg_'+reg+'_jet1_CHadEF_','Lead jet charged hadronic fraction',0.,1.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_CEmEF",'h_reg_'+reg+'_jet1_CEmEF_','Lead jet charged EM fraction',0.,1.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_PhoEF",'h_reg_'+reg+'_jet1_PhoEF_','Lead jet Photon fraction',0.,1.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_EleEF",'h_reg_'+reg+'_jet1_EleEF_','Lead jet Electron fraction',0.,1.,1,1,0,reg)
            # makeplot(dirname+"reg_"+reg+"_jet1_MuoEF",'h_reg_'+reg+'_jet1_MuoEF_','Lead jet Muon fraction',0.,1.,1,1,0,reg)

            if not 'QCD' in reg:
                makeplot(dirname+"reg_"+reg+"_MET",'h_reg_'+reg+'_MET','Real MET (GeV)',160.,500.,2,0,0,reg)
            else:
                makeplot(dirname+"reg_"+reg+"_MET",'h_reg_'+reg+'_MET','Real MET (GeV)',200.,800.,1,0,0,reg)
            makeplot(dirname+"reg_"+reg+"_njet",'h_reg_'+reg+'_nJet','Number of Jets',-1,5,1,1,0,reg)

            if reg[:2]=='1e':
                makeplot(dirname+"reg_"+reg+"_njet_n_minus_1",'h_reg_'+reg+'_njet_n_minus_1_','Number of Jets (n-1 cuts plot)',-1,12,1,1,0,reg)
                makeplot(dirname+"reg_"+reg+"_unclean_njet_n_minus_1",'h_reg_'+reg+'_unclean_njet_n_minus_1_','Number of Jets without cleaning (n-1 cuts plot)',-1,12,1,1,0,reg)
                makeplot(dirname+"reg_"+reg+"_min_dR_jet_ele_preclean",'h_reg_'+reg+'_min_dR_jet_ele_preclean_','min dR between jets and electron before jet cleaning',0.,6.,1,1,0,reg)
                makeplot(dirname+"reg_"+reg+"_min_dR_jet_ele_postclean",'h_reg_'+reg+'_min_dR_jet_ele_postclean_','min dR between jets and electron after jet cleaning',0.,6.,1,1)
            makeplot(dirname+"reg_"+reg+"_min_dPhi_jet_Recoil",'h_reg_'+reg+'_min_dPhi_jet_Recoil_','min d #phi between jets and recoil',0.,6.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_min_dPhi_jet_MET",'h_reg_'+reg+'_min_dPhi_jet_MET','min d #phi between jets and real MET',0.,6.,1,1,0,reg)

            makeplot(dirname+"reg_"+reg+"_min_dPhi_jet_Recoil_n_minus_1",'h_reg_'+reg+'_min_dPhi_jet_Recoil_n_minus_1_','min d #phi between jets and recoil before d#phi cut',0.,6.,1,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_ntau",'h_reg_'+reg+'_ntau_','Number of Taus',-1,4,1,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_nUncleanTau",'h_reg_'+reg+'_nUncleanTau_','Number of Taus (before cleaning)',-1,6,1,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_ntaucleaned",'h_reg_'+reg+'_ntaucleaned_','Number of Taus (after Tau cleaning)',-1,4,5,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_nele",'h_reg_'+reg+'_nele_','Number of Electrons',-1,5,1,1,0,reg)
            #if reg[0]=='2': makeplot(dirname+"reg_"+reg+"_npho",'h_reg_'+reg+'_npho_','Number of Photons',-1,5,1,1,0,reg)
                #            makeplot([dirname+"reg_"+reg+"_nUncleanEle",'h_reg_'+reg+'_nUncleanEle_','Number of Eles (before cleaning)','-1','6','7','1'])
            #makeplot(dirname+"reg_"+reg+"_nmu",'h_reg_'+reg+'_nmu_','Number of Muons',-1,5,1,1,0,reg)
                #            makeplot([dirname+"reg_"+reg+"_nUncleanMu",'h_reg_'+reg+'_nUncleanMu_','Number of Muons (before cleaning)','-1','6','7','1'])
            makeplot(dirname+"reg_"+reg+"_lep1_pT",'h_reg_'+reg+'_lep1_pT_','Lead Lepton p_{T} (GeV)',0.,500.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_lep2_pT",'h_reg_'+reg+'_lep2_pT_','Second Lepton p_{T} (GeV)',0.,250.,1,1,0,reg)
            #if reg.startswith('1etop'): makeplot(dirname+"reg_"+reg+"_e_pT",'h_reg_'+reg+'_e_pT_','Electron p_{T} (GeV)',0.,500.,1,1,0,reg)         #Top
            #if reg.startswith('1mutop'): makeplot(dirname+"reg_"+reg+"_mu_pT",'h_reg_'+reg+'_mu_pT_','Muon p_{T} (GeV)',0.,500.,1,1,0,reg)           #Top
            makeplot(dirname+"reg_"+reg+"_pho_pT",'h_reg_'+reg+'_pho_pT_','Photon p_{T} (GeV)',0.,500.,1,1,0,reg)
            #if reg[1]=='m': makeplot(dirname+"reg_"+reg+"_lep1_iso",'h_reg_'+reg+'_lep1_iso_','Lead Lepton isolation',0.,800.,1,1,0,reg)
            #if reg[1]=='m': makeplot(dirname+"reg_"+reg+"_lep2_iso",'h_reg_'+reg+'_lep2_iso_','Second Lepton isolation',0.,800.,1,1,0,reg)
            #if reg.startswith('1mutop'): makeplot(dirname+"reg_"+reg+"_mu_iso",'h_reg_'+reg+'_mu_iso_','Muon isolation',0.,800.,1,1,0,reg)            #Top
            makeplot(dirname+"reg_"+reg+"_jet1_pT",'h_reg_'+reg+'_Jet1Pt','Lead Jet p_{T} (GeV)',0.,800.,1,1,0,reg)
            makeplot(dirname+"reg_"+reg+"_jet2_pT",'h_reg_'+reg+'_Jet2Pt','Second Jet p_{T} (GeV)',0.,400.,1,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_lep1_dR_tau",'h_reg_'+reg+'_lep1_dR_tau_','dR b/w tau and lead lepton',0.,6.,120,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_lep2_dR_tau",'h_reg_'+reg+'_lep2_dR_tau_','dR b/w tau and second lepton',0.,6.,120,1,0,reg)
            #makeplot(dirname+"reg_"+reg+"_min_lep_dR_tau",'h_reg_'+reg+'_min_lep_dR_tau_','minimum dR b/w tau and leptons',0.,6.,120,1,0,reg)
        except Exception as e:
            print (e)
            print ("Cannot Plot")
            pass
