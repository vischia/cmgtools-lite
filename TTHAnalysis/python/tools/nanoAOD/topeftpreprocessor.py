from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from copy import copy, deepcopy
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
import ROOT as r 

class topeftpreprocessor(Module):
    def __init__(self ):
        self.branches   = [
            "Lep1_pt","Lep1_eta", "Lep1_phi",
            "Lep2_pt","Lep2_eta", "Lep2_phi",
            "nJet30", 
            "jet1_pt", "jet1_eta", "jet1_phi",
            "jet2_pt", "jet2_eta", "jet2_phi",
        ]

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)

    def analyze(self, event):

        all_leps = [l for l in Collection(event,"GenDressedLepton")]
        selected_leps = [l for l in all_leps if (l.pt>20 and abs(l.eta) < 2.4)]


        all_jets = [j for j in Collection(event, "GenJet")]
        selected_jets = [j for j in all_jets if (abs(j.eta) < 2.4 and j.pt > 30)]

        for j in selected_jets:
            for l in selected_leps:
                if deltaR(l,j)<0.4:
                    selected_jets.remove(j)
                    break

        
        if len(selected_leps) < 2:
            return False

        if len(selected_jets) < 2: 
            return False
        
        allret={}
        for i in range(2):
            allret['Lep%d_pt'%(i+1)] = selected_leps[i].pt
            allret['Lep%d_eta'%(i+1)] = selected_leps[i].eta
            allret['Lep%d_phi'%(i+1)] = selected_leps[i].phi

        for i in range(2):
            allret['jet%d_pt'%(i+1)] = selected_jets[i].pt
            allret['jet%d_eta'%(i+1)] = selected_jets[i].eta
            allret['jet%d_phi'%(i+1)] = selected_jets[i].phi

        allret['nJet30'] = len(selected_jets)
        writeOutput(self, allret)
        return True

topEFTpreprocessor = lambda : topeftpreprocessor()
