from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import ROOT as r 
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

def IsDirty(jets, clean, jet):
    # gets a jet and checks whether its not cleaned
    for j in clean:
        if  deltaR(j,jet)<0.01 and abs(j.pt-jet.pt) < 0.1: return False
    return True

def vpSetToVec(vp,verbose=False):
    # for sure theres a better way of doing this...
    vec = r.vector('edm::ParameterSet')()
    
    for pset in vp:
        a   = r.edm.ParameterSet() 
        for par in pset.parameterNames_():
            if verbose: print par, pset.getParameter(par).configValue()
            a.addParameter('std::string')( par, pset.getParameter(par).configValue().replace("'",""))
        vec.push_back(a)

    return vec

def getLorentz(pat):
    vec = r.TLorentzVector()
    vec.SetPtEtaPhiM( pat.pt(), pat.eta(), pat.phi(), pat.mass())
    return vec


class TopRecoSemiLept(Module):
    def __init__(self, constraints):
        # using 2011 resolutions for the moment...
        # these constraints can be used
        # r.TtSemiLepKinFitter.kWLepMass       
        # r.TtSemiLepKinFitter.kTopHadMass       
        # r.TtSemiLepKinFitter.kTopLepMass     
        # r.TtSemiLepKinFitter.kNeutrinoMass   
        # r.TtSemiLepKinFitter.kEqualTopMasses 

        
        from CMGTools.TTHAnalysis.tools.stringResolutions_etEtaPhi_Fall11_cff import  udscResolutionPF
        from CMGTools.TTHAnalysis.tools.stringResolutions_etEtaPhi_Fall11_cff import  bjetResolutionPF
        from CMGTools.TTHAnalysis.tools.stringResolutions_etEtaPhi_Fall11_cff import  muonResolution  
        from CMGTools.TTHAnalysis.tools.stringResolutions_etEtaPhi_Fall11_cff import  elecResolution  
        from CMGTools.TTHAnalysis.tools.stringResolutions_etEtaPhi_Fall11_cff import  metResolutionPF 


        self.inputlabel='_Recl'
        self.listOfBranches = [
            'mtop_reco_Fake',
            'mtop_fitted_reco_Fake',
            'minChi2',
            ]

        # setting up the constraints 
        constr = r.vector('TtSemiLepKinFitter::Constraint')()
        for con in constraints:
            constr.push_back( getattr(r.TtSemiLepKinFitter, con))

        
        # setting up resolutions
        udscResolutions = vpSetToVec(udscResolutionPF.functions)
        bResolutions    = vpSetToVec(bjetResolutionPF.functions)
        eleResolutions  = vpSetToVec(muonResolution  .functions)
        muoResolutions  = vpSetToVec(elecResolution  .functions)
        metResolutions  = vpSetToVec(metResolutionPF .functions)


        jetEnergyResolutionScaleFactors = r.vector('double')(); 
        jetEnergyResolutionEtaBinning   = r.vector('double')(); 
        jetEnergyResolutionScaleFactors.push_back(1.)
        jetEnergyResolutionEtaBinning.push_back(0.)
        jetEnergyResolutionEtaBinning.push_back(-1.)
        
        # calling the kinematic fitter constructors
        self.topRecoMuo = r.TtSemiLepKinFitter(r.TtSemiLepKinFitter.kEtEtaPhi, r.TtSemiLepKinFitter.kEtEtaPhi, r.TtSemiLepKinFitter.kEtEtaPhi,200, 5e-5, 1e-4, constr, 80.4, 173, udscResolutions, bResolutions, muoResolutions, metResolutions, jetEnergyResolutionScaleFactors, jetEnergyResolutionEtaBinning) 
        self.topRecoEle = r.TtSemiLepKinFitter(r.TtSemiLepKinFitter.kEtEtaPhi, r.TtSemiLepKinFitter.kEtEtaPhi, r.TtSemiLepKinFitter.kEtEtaPhi, 200, 5e-5, 1e-4, constr,80.4, 173, udscResolutions, bResolutions, muoResolutions, metResolutions,  jetEnergyResolutionScaleFactors, jetEnergyResolutionEtaBinning)

    def listBranches(self):
        return self.listOfBranches

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print self.listOfBranches
        declareOutput(self, wrappedOutputTree, self.listOfBranches)

    def __call__(self,event):
        return self.run(event, CMGCollection, "met")

    def analyze(self,event):
        writeOutput(self, self.run(event, NanoAODCollection, "MET"))
        return True

    def run(self,event, Collection, metcollection):

        allret = {}

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        cleanJets = [j for j in Collection(event,"JetSel_Recl","nJetSel_Recl")]
        cleanJets  = filter( lambda x : x.pt > 25, cleanJets)

        lightJets  = filter( lambda x : x.btagDeepFlavB < _btagWPs["DeepFlav_%d_%s"%(event.year,"M")][1], cleanJets)
        bJets      = filter( lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"L")][1], cleanJets)
        
        if len(cleanJets) < 4 or len(leps) < 2: 
            for var in self.listOfBranches: allret[var] = -99
            return allret

        
        # potential candidates
        tt_cand = []
        nCandidates = 0 
        for l1 in leps[:2]: # try each lepton as a fake candidate
            for l2 in leps[:2]: # try each remaining lepton as the prompt candidate
                if l1 == l2: continue
                for b in (bJets if len(bJets) else lightJets)[:3]:
                    for j1 in (bJets+lightJets)[:3]:
                        if b == j1: continue
                        for j2 in (bJets+lightJets)[:3]:
                            if b==j2 or j1==j2: continue
                            if (bJets+lightJets).index(j2) < (bJets+lightJets).index(j1): continue 
                            nCandidates = nCandidates + 2
                            # fake comes from the hadronic top
                            t_had = [j1,j2,l1]; t_lep = [l2, b]
                            tt_cand.append( (t_had, t_lep) )
                            # fake comes from the leptonic top
                            t_had =[j1,j2,b]; t_lep = [l2,l1]
                            tt_cand.append( (t_had, t_lep) )


        if not len(tt_cand):
            for var in self.listOfBranches: allret[var] = -9
            return allret

        allChis = []; minChi = 9999

        for can in tt_cand:
            p4HadP = can[0][0].p4()
            p4HadQ = can[0][1].p4()
            p4HadB = can[0][2].p4()
            p4Lepton = can[1][0].p4()
            p4LepB   = can[1][1].p4()

            p4Neutrino = r.TLorentzVector(); p4Neutrino.SetPtEtaPhiM( getattr(event,'%s_pt'%metcollection), 0, getattr(event,'%s_phi'%metcollection), 0)
            leptonCharge = -abs(can[1][0].pdgId)/(can[1][0].pdgId)

            if   abs( can[1][0].pdgId ) == 13:
                fitter, typ =  self.topRecoMuo, r.CovarianceMatrix.kMuon
            elif abs( can[1][0].pdgId ) == 11:
                fitter, typ =  self.topRecoEle, r.CovarianceMatrix.kElectron

            result = fitter.fit(p4HadP, p4HadQ, p4HadB, p4LepB,p4Lepton, p4Neutrino, leptonCharge, typ)
                
            if result == 0:
                allChis.append(  fitter.fitS() ) 
                if fitter.fitS() < minChi:
                    minChi = fitter.fitS()
                    lst = map(getLorentz, [ fitter.fittedHadB(), fitter.fittedHadP(), fitter.fittedHadQ()])
                    hmass_fitted = (lst[0]+lst[1]+lst[2]).M()                        
                    hmass  = (p4HadP + p4HadQ + p4HadB).M()
                    
                        
        #print 'all the candidates are', min(allChis) if len(allChis) else -99, allChis 
        if len(allChis):
            allret['mtop_fitted_reco_Fake']= hmass_fitted
            allret['mtop_reco_Fake']= hmass
            allret['minChi2']       = minChi
            return allret
        else:
            for var in self.listOfBranches: allret[var] = -9
            return allret

topRecoModule = lambda : TopRecoSemiLept(constraints=['kWHadMass','kWLepMass','kTopLepMass','kTopHadMass'])
