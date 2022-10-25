import os

## this script creates a sub-directory in the tree path for a given module
## and runs the friend tree producer for this module

batch = False
queue = "batch" #"batch" for Oviedo, "8nh" or others for lxplus
#path  = "/afs/cern.ch/work/i/igsuarez/public/ewksignals76X_new_copied"
#path  = "/afs/cern.ch/work/m/mdunser/public/HeppyProductions/SUSY_240117/"
#path = "/afs/cern.ch/user/i/igsuarez/work/public/Prod23Jan"
#path = "/pool/ciencias/HeppyTrees/RA7/estructura/Prod23Jan/skimsForRA7"
#outpath = "/pool/cienciasrw/HeppyTrees/RA7/estructura/Prod23Jan/skimsForRA7"

#path = "/pool/ciencias/userstorage/pietro/conversions_skim_rereco/2017-02-25_ewkskims80X_M17_conv_bkg"
#outpath = "/pool/ciencias/userstorage/pietro/conversions_skim_rereco/2017-02-25_ewkskims80X_M17_conv_bkg"

path = "/pool/ciencias/userstorage/pietro/juanSkimsFeb27"
#outpath = "/pool/ciencias/userstorage/pietro/juanSkimsFeb27"
outpath = "/nfs/fanae/user/vischia/checkececee"
force = True # if the friend tree already exists, module is not run; set to True to still run it

## first: module to run, second: list of modules (comma separated) that are required to run
modules = [
          #["leptonJetReCleanerSusyEWK2L" , ""                            ],
          #["leptonJetReCleanerSusyEWK3L" , ""                            ],
          #["bTagEventWeightFullSim2L"                   , "leptonJetReCleanerSusyEWK2L" ],
          ["leptonBuilderEWK"           , "leptonJetReCleanerSusyEWK3L" ],
          #["leptonJetReCleanerSusyRA7"           , "" ],
          #["leptonBuilderRA7"           , "leptonJetReCleanerSusyRA7" ],
          #["bTagEventWeightFastSimRA7"           , "leptonJetReCleanerSusyRA7" ],
          #["bTagEventWeightFullSimRA7"           , "leptonJetReCleanerSusyRA7" ],
          #["leptonJetReCleanerWZSM"           , "" ],
          #["leptonBuilderWZSM"                , "leptonJetReCleanerSusyEWK2L" ],
         ] 

## in case you want to run only specific samples
accept = [
        #'TTWToLNu_ext2_part1',
        #'TTWToLNu_ext1',
        #'TTWToLNu_ext2_part2',
        #'tZq_ll',
        #'TTWToQQ',
        #'WWZ',
        'TTTT',
        'TTGJets',
        'TTJets_SingleLeptonFromTbar',
        #"WZTo3LNu",
          #"WWZ"
          #"50_LO",
          #"WJetsToLNu_LO",
          #"TGJets",
          #"TBar",
          #"TTJets",
          #"tZq",
          #"TTJets_SingleLeptonFromTbar_part1",
          #"TTLL",
          #"TTW",
          #"TTZToLLNuNu",
          #"TTW",
          #"TTWTo",
          #"TTZTo",
          #"TTH",
          #"Tbar",
          #"TTHnobb",
          #"tZq",
          #"VH",
          #"WG",
          #"ZG",
          #"WWZ",
          #"WZZ",
          #"ZZZ",
          #"ZZTo4L",
          #"WWTo2L2Nu",
          #"TTTT",
          #"FromTbar",
          #"romT",
          #"WZTo3LNu_ext",
          #"Run2016B",
          #"GGHZZ",
          #"Run",
          #"T1tttt",
          #"T5qqqq",
          #"T6ttWW",
         ]

#annot open file evVarFriend_SingleMuon_Run2016D_PromptReco_v2_runs_276284_276811.chunk68.root  cannot open file evVarFriend_DoubleEG_Run2016D_PromptReco_v2_runs_276284_276811.chunk14.root

## in case you want to exclude specific samples
exclude = [#"_SS",
           #"_OS",
           #"_TD",
           #"_LO",
           #"Tau",
           #"DoubleMuon_Run2016B_23Sep2016_v3_runs_273150_275376_part",
           #"DoubleEG_Run2016B_23Sep2016_v3_runs_273150_275376_part",
           #"DYJets",
           #"TTJets",
           #"Double",
           #"DoubleEG_Run2016G",
           #"DoubleMuon",
           #"MuonEG",
           #"ZToMuMu",
           #"QCD",
           #"50to",
           #"amcatnlo",
           #"Run",
           #"tZq",
           #"runs_273150_275125",
           #"TTWTo",
           #"TTJets",
           #"WZTo3LNu"
           #"amcatnlo",
           #"T1tttt_1",
           #"WZZ",
           #"JetHT",
           #"MET",
           #"skimmed",
          ]

## --------------- do not touch beyond this line ---------------

def cmd(cmd):
	print cmd
	os.system(cmd)

def mkdir(outpath):
	if os.path.isdir(outpath): return
	cmd("mkdir " + outpath)

def submit(sample, module):
	global batch, queue, path
	super = "python prepareEventVariablesFriendTree.py --tra2 " + path + " " + outpath + "/" + module[0] + " -d " + sample + " --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.multilepFriendTreeProducersToCleanup -m " + module[0]
	if not module[1].strip() == "":
		sm = module[1].strip().split(",")
		for f in sm: super += " -F sf/t " + path + "/" + f + "/evVarFriend_" + sample + ".root"
	if batch:
		super += " --env oviedo -q " + queue + " -N 500000  --log " + outpath + "/" + module[0] + "/log"
		#super += " -q " + queue + " -N 50000"
        else:
                super += " -j 16 "
	cmd(super)


path = path.rstrip("/")
listdir = os.listdir(path)

for module in modules:

	mkdir(outpath + "/" + module[0])
	#mkdir(path + "/" + module[0] + "/log")
	
	for d in listdir:
		if not os.path.isdir(path + "/" + d): continue
		if not ( os.path.exists(path + "/" + d + "/treeProducerSusyMultilepton/tree.root") or os.path.exists(path + "/" + d + "/treeProducerSusyMultilepton/tree.root.url") ): continue
		if not force and os.path.exists(outpath + "/" + module[0] + "/evVarFriend_" + d + ".root"): continue
		if accept  != [] and all([d.find(a) == -1 for a in accept ]): continue
		if exclude != [] and any([d.find(e) >  -1 for e in exclude]): continue
		submit(d, module)

