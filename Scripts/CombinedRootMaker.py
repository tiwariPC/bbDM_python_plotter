import sys,os,array
from ROOT import *

if len(sys.argv)!=2:
    print "Usage: python CombinedRootMaker.py directorypath"
    sys.exit()

fold=sys.argv[1].strip('/')

f=TFile("AllMETHistos.root","RECREATE")
f.cd()

inCRfiles=[fold+"/"+i for i in os.listdir(fold) if i.endswith('hadrecoil.root')]
inSRfiles=[fold+"/"+i for i in ['met_sr1.root','met_sr2.root']]

bins=[200,250,300,400,500,700,1000,2000]

for infile in sorted(inCRfiles+inSRfiles):
    fin=TFile(infile,"READ")
    
    samplist=['DIBOSON','ZJets','GJets','STop','TT','WJets','DYJets','QCD']
    
    if 'sr' in infile:
        samplist.append('bkgSum')
    else:
        samplist.append('data_obs')
    
    if 'sr1' in infile:
        CR="SignalRegion"
        category='1b'
    elif 'sr2' in infile:
        CR="SignalRegion"
        category='2b'
    else:
        reg=infile.split('/')[1].split('_')[1]
        category=reg[-2:]
        if reg.startswith('1mu1e'):
            CR='Top'
        elif reg.startswith('1e'):
            CR='Wenu'
        elif reg.startswith('1mu'):
            CR='Wmunu'
        elif reg.startswith('2e'):
            CR='Zee'
        elif reg.startswith('2mu'):
            CR='Zmumu'
        elif reg.startswith('1gamma'):
            CR='Gamma'
            
    h_tot=fin.Get('bkgSum')
    print
#    print infile
    print "Region: "+CR+category
    tot=h_tot.Integral()
        
    print "Total = "+str(tot)
        
    for samp in samplist:
        h_temp2=fin.Get(samp)
        
        if samp=='bkgSum' or samp=='data_obs':
            sampname='data'
        else:
            sampname=samp
            
        newname="bbDM_2016_"+CR+"_"+sampname+"_"+category       

        h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
        h_temp.SetName(newname)
        h_temp.SetTitle(newname)
        h_temp.SetLineWidth(1)
        h_temp.GetXaxis().SetRangeUser(200,1000)
        h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
        h_temp.SetBinContent(len(bins),0.)
        h_temp.SetMarkerColor(kBlack);
        h_temp.SetMarkerStyle(2);
        sel=h_temp.Integral()  
        f.cd()       
        h_temp.Write()  
            
#        except:
#            sel=0.
#            print "Skipped "+infile+" "+samp 
        
        if tot!=0:
            frac=sel/tot
        else:
            frac=0.
        if samp!="data_obs" and samp!="bkgSum": print "    Sample = " + samp+": Count = %.2f, Fraction = %.4f"%(sel,frac)    
    fin.Close()
    
f.Close()
