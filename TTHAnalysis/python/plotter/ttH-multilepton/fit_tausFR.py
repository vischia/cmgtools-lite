#
# Fit Tau SF with uncertainty 

import ROOT as rt
import sys
import re
import os
import argparse
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from  numpy.linalg import eig
from scipy.odr import *
parser = argparse.ArgumentParser(
                    prog = 'Fit',
                    description = 'fit taus')

parser.add_argument('-d', '--dir', dest="dir")
parser.add_argument( '--year', dest="year",default='all')
parser.add_argument( '--eta', dest="etareg",default='central')  #fwd 

args = parser.parse_args()

lumidic = {'2016APV':'19.5','2016':'16.8','2017':'41.5','2018':'59.7'}

def getPoints(name,sample):
    f = rt.TFile.Open(name,"read")
    g = f.Get("tight_tau_pt_tau_"+sample)
    n = g.GetN()

    xx = []
    yy = []
    yye = []
    for i in range(0,n):
        x = rt.Double(1.)
        y = rt.Double(1.)
        g.GetPoint(i,x,y)
        ye  = g.GetErrorY(i)
        xx.append(x)
        yy.append(y)
        if (y+ye)/y < 1.02:    #if unc in f is lower than 2%, we apply a 2%
           yye.append(1.02*y-y)
        else: 
           yye.append(ye)
    return np.array(xx),np.array(yy),np.array(yye)

def linear(x,a,b):
    return b*x+a

def linear2(B,x):
    return B[1]*x+B[0]

def SF_fit(SF,SF_e,x):

    params, cov = curve_fit(linear,x,SF,sigma=SF_e,absolute_sigma=True)
    return params[0],params[1], cov

def SF_fit_alt(SF,SF_e,x):
    x_err = [0.1]*len(x)
    linear_model = Model(linear2)
    data = RealData(x, SF, sx=x_err, sy=SF_e)
    odr = ODR(data, linear_model, beta0=[0.4, 0.4])
    out = odr.run()
    c0,c1,cov, = out.Output()
    return c0,c1,cov


def Get_Fitted_SF(year,eta):
    #read from TGraph
    x_data,y_data,yerr_data = getPoints(args.dir+"/"+year+"_eta"+eta,"data")
    x_mc,y_mc,yerr_mc= getPoints(args.dir+"/"+year+"_eta"+eta,"TT_true")

    SF = y_data/y_mc
    SF_e = yerr_data/y_mc + y_data*yerr_mc/(y_mc**2)

    print('SF',SF)
    print('sfERR',SF_e)
    print('x',x_data)

    #fitting...
    c0,c1,cov = SF_fit(SF,SF_e,x_data)
    print(c0)
    print(c1)
    print(cov)


    eigenvalues, eigenvectors = eig(cov)
    print('eige',eigenvalues,eigenvectors)
    #eval y using fit:
    y_fit = c1*x_data+c0

    lv0 = np.sqrt(abs(eigenvalues.dot(eigenvectors[0])))
    lv1 = np.sqrt(abs(eigenvalues.dot(eigenvectors[1])))
    #systunc_up = (1 + lv0)*c0 + (1 + lv1)*c1*x_data
    #systunc_dn = (1 - lv0)*c0 + (1 - lv1)*c1*x_data
    ##systunc_1st_up =  (c0 + lv0) + c1*x_data
    ##systunc_1st_dn =  (c0 - lv0) + c1*x_data
    ##systunc_2nd_up =  c0 + (c1 + lv1)*x_data
    ##systunc_2nd_dn =  c0 + (c1 - lv1)*x_data
    l0 =  eigenvalues[0]
    l1 =  eigenvalues[1]
    v00 = eigenvectors[0][0]
    v01 = eigenvectors[0][1]
    v10 = eigenvectors[1][0]
    v11 = eigenvectors[1][1]
    print(l0,l1,v00,v01,v10,v11)
    perr = np.sqrt(np.diag(cov))
    print(perr)
    print(lv0,lv1)
    systunc_1st_up = c0 + np.sqrt(l0)*v00   +  (c1 + np.sqrt(l0)*v01)*x_data
    systunc_1st_dn = c0 - np.sqrt(l0)*v00   +  (c1 - np.sqrt(l0)*v01)*x_data
    systunc_2nd_up = c0 + np.sqrt(l1)*v10   +  (c1 + np.sqrt(l1)*v11)*x_data
    systunc_2nd_dn = c0 - np.sqrt(l1)*v10   +  (c1 - np.sqrt(l1)*v11)*x_data
    print('           c0,c1')
    print('nom',c0,c1)
    print('up1',c0 + np.sqrt(l0)*v00,(c1 + np.sqrt(l0)*v01))
    print('up2',c0 + np.sqrt(l1)*v10,(c1 + np.sqrt(l0)*v01))
    #systunc_1st_up =  (1 + perr[0])*c0 + c1*x_data
    #systunc_1st_dn =  (1 - perr[0])*c0 + c1*x_data
    #systunc_2nd_up =  c0 + (1 + perr[1])*c1*x_data
    #systunc_2nd_dn =  c0 + (1 - perr[1])*c1*x_data
    
    #create root function for output
    func_nominal = rt.TF1("nominal_"+eta,"[0]+[1]*x",0.,200.)
    func_up_1st  = rt.TF1("up_1st_"+eta,"[0]+[1]*x",0.,200.)
    func_dn_1st  = rt.TF1("down_1st_"+eta,"[0]+[1]*x",0.,200.)
    func_up_2nd  = rt.TF1("up_2nd_"+eta,"[0]+[1]*x",0.,200.)
    func_dn_2nd  = rt.TF1("down_2nd_"+eta,"[0]+[1]*x",0.,200.)

    func_nominal.SetParameter(0,c0)
    func_nominal.SetParameter(1,c1)

    func_up_1st.SetParameter(0,c0 + np.sqrt(l0)*v00)
    func_up_1st.SetParameter(1,c1 + np.sqrt(l0)*v01)
    func_dn_1st.SetParameter(0,c0 - np.sqrt(l0)*v00)
    func_dn_1st.SetParameter(1,c1 - np.sqrt(l0)*v01)

    func_up_2nd.SetParameter(0,c0 + np.sqrt(l1)*v10)
    func_up_2nd.SetParameter(1,c1 + np.sqrt(l0)*v01)
    func_dn_2nd.SetParameter(0,c0 - np.sqrt(l1)*v10)
    func_dn_2nd.SetParameter(1,c1 - np.sqrt(l0)*v01)
    functions = [func_nominal,func_up_1st,func_dn_1st,func_up_2nd,func_dn_2nd]
 
    return x_data,SF,SF_e,y_fit,systunc_1st_up,systunc_1st_dn,systunc_2nd_up,systunc_2nd_dn, functions

if args.year == 'all':
   for y in ["2016APV","2016","2017","2018"]: 

      function = []
      for eta in ["central","fwd"]:
        x,SF,SF_err,y_fit,systunc1_up,systunc1_dn,systunc2_up,systunc2_dn,functions = Get_Fitted_SF(y,eta)

        plt.errorbar(x, SF,yerr=SF_err,marker='s', ls ='' )
        plt.plot(x, y_fit, '--k', label = "Nominal Fit" )
        plt.plot(x, systunc1_up, '-.r', label = "1st Eigenvalue" )
        plt.plot(x, systunc1_dn, '-.r' )
        plt.plot(x, systunc2_up, '-.b', label = "2nd Eigenvalue" )
        plt.plot(x, systunc2_dn, '-.b' ) 

        plt.gca().set_ylim(0.55,1.8)   


        ylo,yhi = plt.gca().get_ylim()
        xlo,xhi = plt.gca().get_xlim()        
        print("limits ACIS", ylo,yhi,xlo,xhi)
        plt.text(xlo+3, yhi+0.02, 'CMS', dict(size=15),weight='bold')
        plt.text(xlo+3+18, yhi+0.02, 'Preliminary', dict(size=15),style='italic')

        if eta == "central":
           plt.text(xlo+3, yhi-0.08, r'$|\eta| \leq 1.479$', dict(size=15))
        elif eta == "fwd":
           plt.text(xlo+3, yhi-0.08, r'$|\eta| > 1.479$', dict(size=15))
        lumi = lumidic[y]
        plt.text(xhi-50, yhi+0.02, r'%s $fb^{-1}$ (13 TeV)'%lumi, dict(size=15))
        plt.xlabel(r'$p_T^{\tau_h}$')
        plt.ylabel('SF')
        plt.legend()
        if  not os.path.isdir(args.dir+'/SF_fit/'):
           os.mkdir(args.dir+'/SF_fit/')
        plt.savefig(args.dir+'/SF_fit/'+y+'_'+eta+'.pdf')
        plt.clf()
        print('Plot created: '+args.dir+'/SF_fit/'+y+'_'+eta+'.pdf')

        for fun in functions:
            function.append(fun)
      fout = rt.TFile.Open(args.dir+'/SF_fit/TauSF_'+y+'_fit.root',"recreate")  
      for f in function:
          f.Write()
      fout.Close()

else:
   x,SF,SF_err,y_fit,systunc1_up,systunc1_dn,systunc2_up,systunc2_dn,functions = Get_Fitted_SF(args.year,args.etareg)
   print('sf',y_fit)
   print('var2',systunc2_up)
   plt.errorbar(x, SF,yerr=SF_err,marker='s', ls ='' )
   plt.plot(x, y_fit, '--k', label = "Nominal Fit")
   plt.plot(x, systunc1_up, '-.r', label = "1st Eigenvalue" )
   plt.plot(x, systunc1_dn, '-.r' )
   plt.plot(x, systunc2_up, '-.b', label = "2nd Eigenvalue" )
   plt.plot(x, systunc2_dn, '-.b' ) 
   plt.xlabel(r'$p_T^\tau_h$')
   plt.ylabel('SF')
   if not os.path.isdir(args.dir+'/SF_fit/'):
      os.mkdir(args.dir+'/SF_fit/')
   plt.savefig(args.dir+'/SF_fit/'+args.year+'_'+args.etareg+'.png')
   print('Plot created: '+args.dir+'/SF_fit/'+args.year+'_'+args.etareg+'.png')
    

