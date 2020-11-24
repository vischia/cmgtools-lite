#include "TMath.h"
#include <assert.h>
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"

int nJB(int nJ, float nBJ) {
    int bin = 0;
    
    // Push SRs to make room for the new bins
    if (nJ==1) bin =  1+nBJ;
    if (nJ==2) bin =  3+nBJ;
    if (nJ==3) bin =  6+nBJ;
    if (nJ>=4) bin = 10+nBJ;
    
    return bin;
}

Float_t WZdeltaPhi(Float_t phi1, Float_t phi2)
{
  Float_t res(phi1 - phi2);
  while(res >   M_PI) res -= Float_t(2*M_PI);
  while(res <= -M_PI) res += Float_t(2*M_PI);
  return res;
}

Float_t baseDeltaR(Float_t eta1, Float_t phi1, Float_t eta2, Float_t phi2)
{
  Float_t res;
  Float_t dEta(std::abs(eta1-eta2));
  Float_t dPhi(WZdeltaPhi(phi1, phi2));
  res= std::sqrt(dEta*dEta + dPhi*dPhi);
  return res;
}

Bool_t allTight(Bool_t isT1, Bool_t isT2){
  return isT1 && isT2;
}


Bool_t allTight(Bool_t isT1, Bool_t isT2, Bool_t isT3){
  return isT1 && isT2 && isT3;
}

Bool_t allTight(Bool_t isT1, Bool_t isT2, Bool_t isT3, Bool_t isT4){
  return isT1 && isT2 && isT3 && isT4;
}

Int_t DiFakeRateBin(float pt1, float eta1, float pt2, float eta2, int pdgcode, int tightcode, int ptbin, int etabin)
{
 // First lepton is the one "in range", second lepton is "off range"
 // Returns flavorcode*4 + tightcode
 // Flavor code:
 // -1 == No lepton in range
 //   0 == ee
 //   1 == em
 //   2 == me
 //   3 == mm
 // Tight code:
 //   0 = Tight (in) Tight (out)
 //   1 = Loose (in) Tight (out)
 //   2 = Tight (in) Loose (out)
 //   3 = Loose (in) Loose (out)
  float ptmin; float ptmax; float etamax; float etamin;
 if (ptbin == 0){
   ptmax = 40;
   ptmin = 20;
 } 
 if (etabin == 0){
   etamax = 2.5;
   etamin = -2.5;
 }
 if (pt1 <= ptmax &&  pt1 >= ptmin && eta1 <= etamax && eta1 >= etamin && !( pt2 > ptmax ||  pt2 < ptmin || eta2 > etamax || eta2 < etamin )){
    // First one passes, second doesn't
    return pdgcode*4+tightcode;
 }
 if (pt2 <= ptmax &&  pt2 >= ptmin && eta2 <= etamax && eta2 >= etamin && !( pt1 > ptmax ||  pt1 < ptmin || eta1 > etamax || eta1 < etamin )){
    // Second one passes, first doesn't
    int newpdgcode;
    int newtightcode;
    if (pdgcode == 1) newpdgcode = 2;
    if (pdgcode == 2) newpdgcode = 1;
    if (tightcode == 1) newtightcode = 2;
    if (tightcode == 2) newtightcode = 1;
    return newpdgcode*4+newtightcode;
 }
 // If here, no candidate lepton
 return -1;   
}

//                balance = self.bestOSPair.l1.p4()
//                balance += self.bestOSPair.l2.p4()
//                self.ret["deltaR_WZ"] = deltaR(balance.Eta(), balance.Phi(), self.lepSelFO[i].p4().Eta(), self.lepSelFO[i].p4().Phi())
//                balance -= self.lepSelFO[i].p4()
//                metmom = ROOT.TLorentzVector()
//                metmom.SetPtEtaPhiM(self.met[0],0,self.metphi[0],0)
//                balance -= metmom
//                # Later do it with standalone function like makeMassMET
//                self.ret["wzBalance_pt"] = balance.Pt()
//                balance = self.bestOSPair.l1.p4(self.bestOSPair.l1.conePt)
//                balance += self.bestOSPair.l2.p4(self.bestOSPair.l2.conePt)
//                balance -= self.lepSelFO[i].p4(self.lepSelFO[i].conePt)
//                balance -= metmom
//                self.ret["wzBalance_conePt"] = balance.Pt()
//


// TBD: implement the same but with conePt
Float_t WZbalance(Float_t zpt, Float_t zeta, Float_t zphi, Float_t zm, Float_t wpt, Float_t weta, Float_t wphi, Float_t wm)
{
  TLorentzVector z; z.SetPtEtaPhiM(zpt, zeta, zphi, zm);
  TLorentzVector w; w.SetPtEtaPhiM(wpt, weta, wphi, wm);
  TLorentzVector balance = z + w;
  return balance.Pt();
}

Float_t WZdeltaR(Float_t zeta, Float_t zphi, Float_t weta, Float_t wphi)
{
  ///// save time //TLorentzVector  w; w.SetPtEtaPhiM(wpt ,  weta,  wphi,  wm);
  //
  //Float_t res(baseDeltaR(z.Eta(), z.Phi(), weta, wphi));
  Float_t res(baseDeltaR(zeta, zphi, weta, wphi));
  //std::cout << baseDeltaR(z.Eta(), z.Phi(), weta, wphi) << std::endl;
  // save time //return deltaR(z.Eta(), z.Phi(), w.Eta(), w.Phi());
  return res;
}

Int_t getWZRegion(Float_t met_pt, Float_t mll_3l, Float_t m3L, Int_t nBJetMedium30, Int_t nLepSel, Int_t LepSel4_isTight, Float_t LepSel4_pt){
  //Region index in the WZ analysis: SR->0; CRDY->1; CRTT->2; CRZZ->3; CRconv->4
  if (met_pt > 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel<4  && m3L > 100)                        return 1;
  else if (met_pt <= 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel<4  && m3L > 100)                  return 0;
  else if (met_pt > 30    && nBJetMedium30 > 0  && abs(91.1876-mll_3l)>5   &&  nLepSel<4  && m3L > 100)                   return 2;
  else if (met_pt > 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel==4 && m3L > 100  && LepSel4_isTight && LepSel4_pt > 10)     return 3;
  else if (met_pt <= 30   && nBJetMedium30 == 0 && abs(91.1876-mll_3l)>15  && m3L <= 100  &&  nLepSel<4)     return 4;
  else return -1;
}


/*Int_t getWWWRegion(Float_t met_pt, Float_t mllSFAS, Float_t mllSFOS, Int_t nOSSF, Float_t dPhi3lMet){
  //Region index in the WZ analysis: SR->0; CRDY->1; CRTT->2; CRZZ->3; CRconv->4
  if (met_pt > 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel<4  && m3L > 100)                        return 0;
  else if (met_pt <= 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel<4  && m3L > 100)                  return 1;
  else if (met_pt > 30    && nBJetMedium30 > 0  && abs(91.1876-mll_3l)>5   &&  nLepSel<4  && m3L > 100)                   return 2;
  else if (met_pt > 30    && nBJetMedium30 == 0 && abs(91.1876-mll_3l)<15  &&  nLepSel==4 && m3L > 100  && LepSel4_isTight && LepSel4_pt > 10)     return 3;
  else if (met_pt <= 30   && nBJetMedium30 == 0 && abs(91.1876-mll_3l)>15  && m3L <= 100  &&  nLepSel<4)     return 4;
  else return -1;
}*/




Float_t WZ_weight_W16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.482; Float_t fRSM = 0.272; Float_t fOSM = 0.246;
    Float_t den = 3./8. *( (1 -c)*(1-c)*fLSM + (1+c)*(1+c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1-c)*(1-c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1+c)*(1+c)*fRSM/den;
}

Float_t WZ_weight_Wp16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.538; Float_t fRSM = 0.233; Float_t fOSM = 0.229;
    Float_t den = 3./8. *( (1 -c)*(1-c)*fLSM + (1+c)*(1+c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1-c)*(1-c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1+c)*(1+c)*fRSM/den;
}


Float_t WZ_weight_Wm16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.392; Float_t fRSM = 0.331; Float_t fOSM = 0.277;
    Float_t den = 3./8. *( (1 -c)*(1-c)*fLSM + (1+c)*(1+c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1-c)*(1-c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1+c)*(1+c)*fRSM/den;
}


Float_t WZ_weight_Z16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.314; Float_t fRSM = 0.426; Float_t fOSM = 0.260;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}

Float_t WZ_weight_Zm16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.288; Float_t fRSM = 0.466; Float_t fOSM = 0.246;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}

Float_t WZ_weight_Zp16(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.331; Float_t fRSM = 0.401; Float_t fOSM = 0.269;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}


Float_t WZ_weight_Z(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.314; Float_t fRSM = 0.424; Float_t fOSM = 0.262;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}

Float_t WZ_weight_ZP(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.335; Float_t fRSM = 0.389; Float_t fOSM = 0.275;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}


Float_t WZ_weight_ZM(Float_t c, Int_t mode)
{
    Float_t fLSM = 0.278; Float_t fRSM = 0.481; Float_t fOSM = 0.242;
    Float_t alpha = 0.213;
    Float_t den = 3./8. *( (1 -2*c*alpha + c*c)*fLSM + (1 +2*c*alpha + c*c)*fRSM + 2*(1-c*c)*fOSM);
    if (mode ==  0) return 3./4.*(1-c*c)*fOSM/den;
    if (mode == -1) return 3./8.*(1 -2*c*alpha + c*c)*fLSM/den;
    if (mode ==  1) return 3./8.*(1 +2*c*alpha + c*c)*fRSM/den;
}


float unrealnessW(Float_t ptl, Float_t etal, Float_t phil, Float_t ptnu, Float_t phinu){
   Float_t muVal = (80.385)*(80.385)/2. + ptl*ptnu*TMath::Cos(phil-phinu);
   Float_t disc  = (muVal*muVal*ptl*ptl*TMath::SinH(etal)*TMath::SinH(etal)/(ptl*ptl*ptl*ptl) - ((ptl*ptl*TMath::CosH(etal)*TMath::CosH(etal))*ptnu*ptnu - muVal*muVal)/ptl*ptl);        
   return disc;
}

void functionsWZ() {}