#!/usr/bin/python

# import ROOT in batch mode
import sys
import argparse
import math

def readFile(inputfile):
    f = open(inputfile, 'r')
    obs = []
    bkg = []
    for line in f:
        if line.startswith('BACKGROUND'): 
            bkg = line.split()
        if 'DATA' in line:
            obs = line.split()

    return bkg,obs

def nsf(num, n=2):
    if (num<100): 
        return "{0:.2g}".format(num)
    else:   
        return "{0:.0f}".format(round(int(num)/10)*10)
        
    return -999.
    
def getBackground(array):
    exp = [0  for i in range(18)]
    err = [0  for i in range(18)]
    stat = [0  for i in range(18)]
    syst = [0  for i in range(18)]
    
    tmp =[]
    for i,y in enumerate(array):
        if '+/-' in y:  continue
        if 'stat' in y: continue
        if 'syst' in y: continue
        tmp.append(y)
            
    for i in range(18):
        index = i*3
        exp[i]  = nsf(float(tmp[index]),2)
        stat[i] = float(tmp[index+1])
        syst[i] = float(tmp[index+2])
        err[i]  = nsf(math.sqrt(stat[i]*stat[i]+syst[i]*syst[i]),2)
        
    return exp,err
    
def make2lssTable(inputfile):
    (bkg,obs) = readFile(inputfile)
    bkg.pop(0)
    (exp,err) = getBackground(bkg)
    obs.pop(0)
    print "\n\n\n\n"
    print "\\begin{table}[tbh]"
    print "\\centering"
    print "\\caption{Search regions for events with two same-sign light flavor leptons. Uncertainty includes both systematic and statistical.}"
    print "\\label{tab:regionsSS}"
    print "\\resizebox{\\textwidth}{!}{"
    print "\\begin{tabular}{|c|c|c|cc|cc|cc|}"
    print "\\hline\\hline"
    print "$N_{jets}$ & \\MT    &  $\\pt^{\\ell\\ell}$ &   \\multicolumn{2}{|c|}{$\\MET < 100\\GeV$} & \\multicolumn{2}{|c|}{$100\\GeV < \\MET < 150\\GeV $} & \\multicolumn{2}{|c|}{$\\MET > 150\\GeV$}\\\\"
    print " &  &   &  exp & obs & exp & obs & exp & obs \\\\  "
    print "\\hline\\hline"
    print "\\multirow{3}{*}{0} & \\multirow{2}{*}{$<100\\GeV$} 	& $<50\\GeV$ & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s \\\\ \\cline{3-9}"  %(exp[0],err[0],obs[0],exp[1],err[1],obs[1],exp[2],err[2],obs[2]) 
    print "                &				 				& $>50\\GeV$ & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s \\\\ \\cline{2-9}"      %(exp[3],err[3],obs[3],exp[4],err[4],obs[4],exp[5],err[5],obs[5])
    print "				   &   		      $>100\\GeV$ 	&    -      & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s\\\\ \\hline"                 %(exp[6],err[6],obs[6],exp[7],err[7],obs[7],exp[7],err[7],obs[7])
    print "\\multirow{3}{*}{1} & \\multirow{2}{*}{$<100\\GeV$} 	& $<50\\GeV$ & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s \\\\ \\cline{3-9}"  %(exp[9],err[9],obs[9],exp[10],err[10],obs[10],exp[11],err[11],obs[11])
    print "                &				 				& $>50\\GeV$ & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s \\\\ \\cline{2-9}"      %(exp[12],err[12],obs[12],exp[13],err[13],obs[13],exp[14],err[14],obs[14])
    print "				   &   		      $>100\\GeV$ 	&    -      & %s $\pm$ %s & %s & %s $\pm$ %s & %s & %s $\pm$ %s & %s\\\\ \\hline    "             %(exp[15],err[15],obs[15],exp[16],err[16],obs[16],exp[17],err[17],obs[17])
    print "\\end{tabular}}"
    print "\\end{table}"
    print "\n\n\n\n"

#### ========= MAIN =======================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(usage="make2lss.py [options]",description="make table for pass",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--perBin", dest="perBin",default="", help='Input filename')
    
    args = parser.parse_args()
    
    perBin = args.perBin

    make2lssTable(perBin)
    print "DONE"
