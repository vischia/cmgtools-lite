#include "TFile.h"
#include "TH2.h"
#include "TF1.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TRandom3.h"

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <map>

float ttW_charge_asymmetry(int hasOSSF, int nJet, int sign_charge, float lepton_score, float lepton_eta )
{
  int iJet = (nJet < 4) ? 0 : 1;

  // 2 hasOSSF bins 
  // 2 sign_charge_bins

  // 2 lepton score bins
  int iLeptonScore=0;
  if (lepton_score < 0.1) iLeptonScore=0;
  else
                    iLeptonScore=1;
  // 4 lepton_eta bins
  int iLeptonEta=0;
  if      (lepton_eta < -0.5) iLeptonEta=0;
  else if (lepton_eta < 0.  ) iLeptonEta=1;
  else if (lepton_eta < 0.5 ) iLeptonEta=2;
  else                        iLeptonEta=3;
   
  return iLeptonEta+iLeptonScore*4+iJet*8+hasOSSF*16+(sign_charge < 0)*32;
}

float ttW_charge_asymmetry_simple(int hasOSSF, int nJet, int sign_charge, float lepton_eta )
{
  int iJet = (nJet < 4) ? 0 : 1;

  // 2 hasOSSF bins 
  // 2 sign_charge_bins

  // 4 lepton_eta bins
  int iLeptonEta=0;
  if      (lepton_eta < -0.5) iLeptonEta=0;
  else if (lepton_eta < 0.  ) iLeptonEta=1;
  else if (lepton_eta < 0.5 ) iLeptonEta=2;
  else                        iLeptonEta=3;
   
  return iLeptonEta+iJet*4+hasOSSF*8+(sign_charge < 0)*16;
}

float ttW_charge_asymmetry_simple_withbees(int hasOSSF, int nJet, int sign_charge, float lepton_eta, int nb )
{
  int iJet = (nJet < 4) ? 0 : 1;

  // 2 hasOSSF bins 
  // 2 sign_charge_bins

  // 4 lepton_eta bins
  int iLeptonEta=0;
  if      (lepton_eta < -0.5) iLeptonEta=0;
  else if (lepton_eta < 0.  ) iLeptonEta=1;
  else if (lepton_eta < 0.5 ) iLeptonEta=2;
  else                        iLeptonEta=3;

  // we have double the bins in hasOSSF
  int iBJet = 0;
  if (hasOSSF && iJet==0 && nb > 1){
    iBJet=2;
  }
   
  return iLeptonEta+(iJet+iBJet)*4+hasOSSF*8+(sign_charge < 0)*20;
}

float ttW_charge_asymmetry_simple_withbees_nocharge(int hasOSSF, int nJet, float lepton_eta, int nb )
{
  int iJet = (nJet < 4) ? 0 : 1;

  // 2 hasOSSF bins 
  // 2 sign_charge_bins

  // 4 lepton_eta bins
  int iLeptonEta=0;
  if      (lepton_eta < -0.5) iLeptonEta=0;
  else if (lepton_eta < 0.  ) iLeptonEta=1;
  else if (lepton_eta < 0.5 ) iLeptonEta=2;
  else                        iLeptonEta=3;

  // we have double the bins in hasOSSF
  int iBJet = 0;
  if (hasOSSF && iJet==0 && nb > 1){
    iBJet=2;
  }
   
  return iLeptonEta+(iJet+iBJet)*4+hasOSSF*8;
}

float ttW_charge_asymmetry_v4(int hasOSSF, int nJet, float lepton_eta, int nb, float mZ )
{
  int iJet = (nJet < 4) ? 0 : 1;

  // 2 hasOSSF bins 
  // 2 sign_charge_bins

  // 4 lepton_eta bins
  int iLeptonEta=0;
  if      (lepton_eta < -0.5) iLeptonEta=0;
  else if (lepton_eta < 0.  ) iLeptonEta=1;
  else if (lepton_eta < 0.5 ) iLeptonEta=2;
  else                        iLeptonEta=3;

  // we have double the bins in hasOSSF
  int iBJet = 0;
  if (hasOSSF && iJet==0 && nb > 1){
    iBJet=2;
  }
  int imZ=0;
  if (hasOSSF){
    if (mZ  > 110) imZ=1;
  }
   
  return iLeptonEta+(iJet+iBJet)*4+hasOSSF*8 + 12*imZ;
}

float ttW_ATLAS_selection( int nJet, int nbjets, float met )
{

  if (nbjets == 1){
    if (met < 50) return -1;
    if (nJet < 4) return 0;
    else return 1;
  }
  else{
    if (nJet < 4) return 2;
    else return 3;
  }
  
}
