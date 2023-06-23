#!/usr/bin/env python
import sys
import re
import os

ODIR=sys.argv[1]
YEAR=sys.argv[2]
lumis = {
    '2016APV': '19.5',
    '2016': '16.8',
    '2017': '41.5',
    '2018': '59.7',
    'all' : '19.5,16.8,41.4,59.7',
}


submit = '{command}' 
dowhat = "eff" 
dojeccomps=True
P0="/eos/cms/store/cmst3/group/tthlep/peruzzi/"
#if 'cmsco01'   in os.environ['HOSTNAME']: P0="/data1/peruzzi"
nCores = 8
if 'fanae' in os.environ['HOSTNAME']:
    nCores = 32
    #submit = 'sbatch -c %d -p cpupower  --wrap "{command}"'%nCores
    P0     = "/beegfs/data/nanoAODv9/ttH_differential/"
if 'gae' in os.environ['HOSTNAME']: 
    P0     = "/beegfs/data/nanoAODv9/ttH_differential/"

if 'cism.ucl.ac.be' in os.environ['HOSTNAME']:
    P0   = "/nfs/user/pvischia/tth/ul/" 

if ".psi.ch" in os.environ['HOSTNAME']:
    P0 = "/pnfs/psi.ch/cms/trivcat/store/user/sesanche"

TREESALL = "--FMCs {P}/0_jmeUnc_v1_new --FMCs {P}/2_scalefactors_lep/ --Fs {P}/3_tauCount_new --FMCs {P}/2_btagSF " 
YEARDIR=YEAR if YEAR != 'all' else ''
TREESONLYFULL     = "-P "+P0+"/NanoTrees_UL_v2_060422_newfts/%s          --Fs  {P}/1_recl_new "%(YEARDIR,)         

def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if dowhat == "eff":  
          print 'python mcEfficiencies.py',"-o %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join([x for x in sys.argv[4:] if x!='forcePlotChoice'])

def base(selection):
    THETREES = TREESALL
    CORE=' '.join([THETREES,TREESONLYFULL])
    CORE+="--s2v -j %d -l %s -L ttH-multilepton/functionsTTH.cc --tree NanoAOD --mcc ttH-multilepton/lepchoice-ttH-FO.txt --year %s "%(nCores, lumis[YEAR],YEAR if YEAR!='all' else '2016APV,2016,2017,2018')# --neg" --s2v 
    RATIO= " --showRatioalt --ratioRange -0.5 0.5 "
    LEGEND=" --legend=LR "
    SPAM=" --ytitle 'Fake rate' "
    if dowhat == "eff": CORE+=RATIO+LEGEND+SPAM
    GO="%s ttH-multilepton/lepton-fr/lepton-mca-fr_tau_studies.txt ttH-multilepton/lepton-fr/make_fake_rates_tau_sels.txt object-studies/lepton-perlep_tau.txt ttH-multilepton/lepton-fr/make_fake_rates_tau_plots.txt"%CORE
    GO="%s -W ''L1PreFiringWeight_Nom*puWeight*btagSF*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId,LepGood1_conePt,LepGood2_pdgId,LepGood2_conePt,2,year,suberaId)'"%GO
    GO = "%s  --xf QCD_Pt20to30_EMEnriched   --groupBy cut --sP tight_tau --sP 'pt_tau'"%GO

    if selection == 'fwd':
       GO="%s  -E eta_fwd --eta fwd"%GO
    elif selection == 'central':
       GO="%s  -E eta_central --eta central"%GO
    return GO

if __name__ == '__main__':

    torun = sys.argv[3]

    if 'fwd' in torun:
        x = base('fwd')
    elif 'central' in torun:
        x = base('central')

    runIt(x,'%s'%torun)

