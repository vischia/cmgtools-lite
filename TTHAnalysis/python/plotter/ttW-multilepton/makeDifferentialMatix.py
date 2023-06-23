import ROOT as r 
import collections
import math 
import os,sys
thelumi = 1. #use the lumi used to normalized the gen histos (fb-1)
folder = sys.argv[1]
GenInfo=folder+"/"+sys.argv[2]
Fit=folder+"/fitDiagnosticsnominal.root"
varn = sys.argv[3]
ws=folder+"/ws_"+varn+".root"

plotformat = (600,600)
height = plotformat[1]
c1 = r.TCanvas("_canvas", '', plotformat[0], height)

r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)

tf=r.TFile.Open(str(GenInfo))
print("open")
tff = r.TFile.Open(Fit)
print("open")
tws = r.TFile.Open(ws)
print("open")
reference=tf.Get("x_TTW_inclusive")
print("open")
varname = {"lep1_pt":"p_{T} (lep)","njets":"N Jet","nbjets":"N b-tag","jet1_pt":"p_{T} (jet)","deta_llss":"#Delta #eta (ll)"}

#get matrix

fitResult = tff.Get('fit_s')

w = tws.Get("w")
print("open")
poiList = r.RooArgList('poiList')
nparticlebins = reference.GetNbinsX()
poinames =  []
count =0 
for v in fitResult.floatParsFinal():
        
        if "r_TTW" in v.GetName():
            count += 1
            poinames.append(v.GetName())
            if count == reference.GetNbinsX(): break

print(poinames)
for poi in poinames:
       var = w.var(poi)
       print(var,poi)
       poiList.add(var)

cov = fitResult.reducedCovarianceMatrix(poiList)



hCov    = r.TH2D('hCovar_{varn}'.format(varn = var), '',
                 nparticlebins, -0.5, nparticlebins - 0.5,
                 nparticlebins, -0.5, nparticlebins - 0.5)

scaleval = 1.
scaleval = 1./(thelumi)

for i in range(1, nparticlebins + 1):
    tmpintx = reference.GetBinContent(i) 
    for j in range(1, nparticlebins + 1):
         tmpinty = reference.GetBinContent(j)
         normx = tmpintx * scaleval
         normy = tmpinty * scaleval

         #normx = 1
         #normy = 1

         cov[i-1][j-1] = cov[i-1][j-1] * normx * normy
         hCov.SetBinContent( hCov.GetBin(i,j), cov[i-1][j-1] )

hCov.GetYaxis().SetTitle("%s"%varname[varn])
hCov.GetXaxis().SetTitle("%s"%varname[varn])
hCov.Draw("colz,text")

plot='matrix_'+varn
c1.SaveAs(folder+'/plot_%s.png'%(plot.replace('.','p')))
