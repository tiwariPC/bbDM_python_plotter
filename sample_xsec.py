import os, sys
#//--------------------------------------------------------------------------------------
def getXsec(samplename):
    Xsec = 1.0
    if 'DYJetsToLL_M-50_HT-100to200'   in samplename: Xsec  = 147.4
    if 'DYJetsToLL_M-50_HT-200to400'   in samplename: Xsec  = 40.99
    if 'DYJetsToLL_M-50_HT-400to600'   in samplename: Xsec  = 5.678
    if 'DYJetsToLL_M-50_HT-600to800'   in samplename: Xsec  = 1.367
    if 'DYJetsToLL_M-50_HT-800to1200'  in samplename: Xsec  = 0.6304
    if 'DYJetsToLL_M-50_HT-1200to2500' in samplename: Xsec  = 0.1514
    if 'DYJetsToLL_M-50_HT-2500toInf'  in samplename: Xsec  = 0.003565

    if 'ZJetsToNuNu_HT-100to200'   in samplename: Xsec  = 280.35
    if 'ZJetsToNuNu_HT-200to400'   in samplename: Xsec  = 77.67
    if 'ZJetsToNuNu_HT-400to600'   in samplename: Xsec  = 10.73
    if 'ZJetsToNuNu_HT-600to800'   in samplename: Xsec  = 2.559
    if 'ZJetsToNuNu_HT-800to1200'  in samplename: Xsec  = 1.1796
    if 'ZJetsToNuNu_HT-1200to2500' in samplename: Xsec  = 0.28833
    if 'ZJetsToNuNu_HT-2500toInf'  in samplename: Xsec  = 0.006945

    if 'WJetsToLNu_HT-70to100'    in samplename: Xsec  = 1372.0
    if 'WJetsToLNu_HT-100to200'   in samplename: Xsec  = 1345.0
    if 'WJetsToLNu_HT-200to400'   in samplename: Xsec  = 359.7
    if 'WJetsToLNu_HT-400to600'   in samplename: Xsec  = 48.91
    if 'WJetsToLNu_HT-600to800'   in samplename: Xsec  = 12.05
    if 'WJetsToLNu_HT-800to1200'  in samplename: Xsec  = 5.501
    if 'WJetsToLNu_HT-1200to2500' in samplename: Xsec  = 1.329
    if 'WJetsToLNu_HT-2500toInf'  in samplename: Xsec  = 0.03216

    if 'GJets_HT-40To100'    in samplename: Xsec  = 20790
    if 'GJets_HT-100To200'   in samplename: Xsec  = 9238
    if 'GJets_HT-200To400'   in samplename: Xsec  = 2305
    if 'GJets_HT-400To600'   in samplename: Xsec  = 274.4
    if 'GJets_HT-600ToInf'   in samplename: Xsec  = 93.46

    if 'QCD_HT500To700'    in samplename: Xsec  = 32100
    if 'QCD_HT700to1000'   in samplename: Xsec  = 6831
    if 'QCD_HT1000to1500'  in samplename: Xsec  = 1207
    if 'QCD_HT1500to2000'  in samplename: Xsec  = 119.9
    if 'QCD_HT2000toInf'   in samplename: Xsec  = 25.24

    if 'TT_TuneCUETP8M2T4' in samplename: Xsec = 831.76
    if 'TTToSemilepton'    in samplename: Xsec = 364.35
    if 'TTTo2L2Nu'         in samplename: Xsec = 87.31

    if 'WWTo1L1Nu2Q_13TeV' in samplename: Xsec = 49.997
    if 'WWTo2L2Nu_13TeV'   in samplename: Xsec = 12.178
    if 'WWTo4Q_4f_13TeV'   in samplename: Xsec = 51.723

    if 'WZTo1L1Nu2Q_13TeV' in samplename: Xsec = 10.71
    if 'WZTo1L3Nu_13TeV'   in samplename: Xsec = 3.0330
    if 'WZTo2L2Q_13TeV'    in samplename: Xsec = 5.5950
    if 'WZTo2Q2Nu_13TeV'   in samplename: Xsec = 6.4880
    if 'WZTo3LNu'          in samplename: Xsec = 4.4297

    if 'ZZTo2L2Q_13TeV'    in samplename: Xsec = 3.22
    if 'ZZTo2Q2Nu_13TeV'   in samplename: Xsec = 4.04
    if 'ZZTo4L_13TeV'      in samplename: Xsec = 1.2120
    if 'ZZTo4Q_13TeV'      in samplename: Xsec = 6.842

    if 'ST_s-channel_4f_leptonDecays' in samplename: Xsec = 3.36
    if 'ST_t-channel_antitop_4f'      in samplename: Xsec = 80.95
    if 'ST_t-channel_top_4f'          in samplename: Xsec = 136.02
    if 'ST_tW_antitop_5f'             in samplename: Xsec = 35.85
    if 'ST_tW_top_5f'                 in samplename: Xsec = 35.85


    return Xsec
