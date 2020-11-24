import os

base = "python makeShapeCardsSusy.py RunII_SUSY_EWK/2016/3l/mca_ewkino_v5_lepgood.txt RunII_SUSY_EWK/2016/3l/cuts_3l_lepgood.txt 'SR3lAfromlepgood(MET_pt_nom,mass_2(LepGood_pt[0], LepGood_eta[0], LepGood_phi[0], LepGood_mass[0], LepGood_pt[1], LepGood_eta[1], LepGood_phi[1], LepGood_mass[1]),  mass_2(LepGood_pt[0], LepGood_eta[0], LepGood_phi[0], LepGood_mass[0], LepGood_pt[2], LepGood_eta[2], LepGood_phi[2], LepGood_mass[2]),  mass_2(LepGood_pt[2], LepGood_eta[2], LepGood_phi[2], LepGood_mass[2], LepGood_pt[1], LepGood_eta[1], LepGood_phi[1], LepGood_mass[1]),  mt_2(LepGood_pt[0], LepGood_phi[0], MET_pt_nom, MET_phi_nom),  mt_2(LepGood_pt[1], LepGood_phi[1], MET_pt_nom, MET_phi_nom),  mt_2(LepGood_pt[2], LepGood_phi[2], MET_pt_nom, MET_phi_nom),encodepdg(LepGood_pdgId[0], LepGood_pdgId[1], LepGood_pdgId[2]))' '44,0.5,44.5' RunII_SUSY_EWK/systs/systs_wz16_lepgood.txt --tree treeProducerSusyMultilepton -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_2016_skimWZ/ -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_2016_signals/ --FFasts {P}/puWeight/ --FFulls {P}/leptonPtCorrections/ --FMCs {P}/trigger_prefiring/ --Fs {P}/leptonJetReCleanerWZSM/ --Fs {P}/leptonBuilderEWK/ --Fs {P}/trigger_2016/  --FMCs {P}/leptonMatcher/ --FMCs {P}/bTagEventWeights/ -L RunII_SM_WZ/functionsWZ.cc -L RunII_SM_WZ/functionsSF.cc -L RunII_SM_WZ/functionsMCMatch.cc -L RunII_SUSY_EWK/functionsEWKcorr.cc   --plotgroup data_fakes+=.*promptsub.* --neglist .*promptsub.* --neg -W 'puWeight*($MC{bTagWeightDeepCSVT_nom} $FASTSIM{bTagWeightDeepCSVT})*weight_PrefiringJets*weight_PrefiringPhotons' --obj Events -j 8 -f  -l 35.9  -E SR3lA  -p prompt.* -p conv.* -p data.* -p fakes.* -p 'sig_TChiWZ_.*'   -X SRevent -A  alwaystrue lepMVA 'allTight(LepGood_mvaTTH[0],LepGood_mvaTTH[1],LepGood_mvaTTH[2],LepGood_pdgId[0],LepGood_pdgId[1],LepGood_pdgId[2], [CUT1],[CUT2])' -o mvael[TAG1]mvamu[TAG2] --od testleptonMVA16_3l_lepgood"

for i in range(20):
  for j in range(20):
    x = -1. + 0.1*i
    y = -1. + 0.1*j
    #print base.replace("[CUT1]", str(x)).replace("[CUT2]", str(y)).replace("[TAG1]", str(x).replace("-","m")).replace("[TAG2]", str(x).replace("-","m"))
    #os.system("sbatch -c 8 -p batch -J" + " --wrap \"" + base.replace("[CUT1]", str(x)).replace("[CUT2]", str(y)).replace("[TAG1]", str(x).replace("-","m")).replace("[TAG2]", str(x).replace("-","m")) + "\"")
    print "sbatch -c 8 -p batch " + " --wrap \"" + base.replace("[CUT1]", str(x)).replace("[CUT2]", str(y)).replace("[TAG1]", str(x).replace("-","m")).replace("[TAG2]", str(y).replace("-","m")).replace("$","\$") + "\""