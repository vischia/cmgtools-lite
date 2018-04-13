cd /nfs/fanae/user/carlosec/CMSSW_8_0_19/src/CMGTools/TTHAnalysis/python/plotter/
source /cms/cmsset_default.sh
cmsenv
python mcPlots.py susy-ewkino/3lfor2017Tests/mca_3l_Test2017.txt susy-ewkino/3lfor2017Tests/cuts_Test2017.txt susy-ewkino/3lfor2017Tests/plots_pt.txt -P /pool/cienciasrw/userstorage/carlosec/ewkTreesfor2017Test/bkg2017 -P /pool/cienciasrw/userstorage/carlosec/ewkTreesfor2017Test/sig --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/3lfor2017Tests/mcc_ewkino.txt --mcc susy-ewkino/mcc_triggerdefs.txt --load-macro susy-ewkino/3l/functionsEWK.cc --load-macro susy-ewkino/functionsSF.cc --load-macro susy-ewkino/functionsPUW.cc -l 35.9 -F sf/t {P}/leptonJetReCleanerSusyEWK3L_lowpt/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK_lowpt/evVarFriend_{cname}.root -W 'puw_nInt_Moriond(nTrueInt) * leptonSF(getLepSF(LepSel_pt[0], LepSel_eta[0], LepSel_pdgId[0], 0), getLepSF(LepSel_pt[1], LepSel_eta[1], LepSel_pdgId[1], 0), getLepSF(LepSel_pt[2], LepSel_eta[2], LepSel_pdgId[2], 0))' --AP -j 16 --mcc susy-ewkino/3lfor2017Tests/deltaTriggers.mcc --load-macro susy-ewkino/3lfor2017Tests/functionsIdealTrigger.cc --pdir /nfs/fanae/user/carlosec/www/ewkPlots2017/_Triggerme2312flav_eee -E Triggerme2312 -E flav_eee --print '' -f
