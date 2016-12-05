#python makeShapeCardsSusy.py susy-ewkino/2lss/mca-2lss-mcdata-frdata.txt susy-ewkino/2lss/cuts_2lss.txt 'SR_ewk_ss2l_HH30(nJet40,LepGood1_conePt,LepGood1_phi, LepGood2_conePt,LepGood2_phi, met_pt,met_phi)' '18,0.5,18.5' susy-ewkino/2lss/systs_ewkino_2lss.txt -P /nfs/fanae/user/nachos/treesfor2LSS --Fs {P}/leptonJetReCleanerSusyEWK2L  --Fs {P}/leptonBuilderEWK --load-macro susy-ewkino/3l/functionsEWK.cc -j 6 -l 35 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/2lss/lepchoice-2lss-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt   -f -p data -p convs -p prompt.* -p fakes.* -p sig.* -W 'puw2016_nTrueInt_13fb(nTrueInt)*triggerSF(4,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,0,0)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)'  --pgroup prompt_ttX+=prompt_ttW --pgroup prompt_ttX+=prompt_ttZ --pgroup prompt_ttX+=prompt_ttH --od ~/Datacards2lSS_HH30 -o testDatacardSR

python makeShapeCardsSusy.py susy-ewkino/2lss/mca-2lss-mcdata-frdata.txt susy-ewkino/2lss/cuts_2lss.txt 'met_pt' '1,0.,400' susy-ewkino/2lss/systs_ewkino_2lss.txt -P /nfs/fanae/user/nachos/treesfor2LSS --Fs {P}/leptonJetReCleanerSusyEWK2L  --Fs {P}/leptonBuilderEWK --load-macro susy-ewkino/3l/functionsEWK.cc -j 10 -l 35 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/2lss/lepchoice-2lss-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt   -f -p data -p convs -p prompt.* -p fakes.* -p sig.* -W 'puw2016_nTrueInt_13fb(nTrueInt)*triggerSF(4,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,0,0)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)'  --pgroup prompt_ttX+=prompt_ttW --pgroup prompt_ttX+=prompt_ttZ --pgroup prompt_ttX+=prompt_ttH --od ~/DatacardsSSR1v3 -o testDatacardSSR1v3 -E 1j -E mtminse100 -E Cutptdil -E met200













#python makeShapeCardsSusy.py susy-ewkino/2lss/mca-2lss-mcdata-frdata.txt susy-ewkino/2lss/cuts_2lss.txt 'SR_ewk_ss2l(nJet40,LepGood1_conePt,LepGood1_phi, LepGood2_conePt,LepGood2_phi, met_pt,met_phi)' '18,0.5,18.5' susy-ewkino/2lss/systs_ewkino_2lss.txt -P /nfs/fanae/user/nachos/treesfor2LSS --Fs {P}/leptonBuilderEWK --Fs {P}/leptonJetReCleanerSusyEWK2L --load-macro susy-ewkino/3l/functionsEWK.cc  -j 6 -l 35 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/2lss/lepchoice-2lss-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt  -f -p data -p convs -p prompt.* -p fakes.* -p sig.* -W 'puw2016_nTrueInt_13fb(nTrueInt)*triggerSF(4,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,0,0)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)'  --pgroup prompt_ttX+=prompt_ttW --pgroup prompt_ttX+=prompt_ttZ --pgroup prompt_ttX+=prompt_ttH --od /nfs/fanae/user/carlosec/CMSSW_7_4_7/Datacard2lss -o testSRICHEP
