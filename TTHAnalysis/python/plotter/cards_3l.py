import os

bin_ranges =[
    ['0', '60', 'bin1'],
#    ['60', '120', 'bin2'],
#    ['120', '200', 'bin3'],
#    ['200', '300', 'bin4'],
#    ['300', '450', 'bin5'],
#    ['450', '1000', 'bin6']
]

for i in range(len(bin_ranges)):
    print str(bin_ranges[i][0]) 
    print str(bin_ranges[i][1])
    print str(bin_ranges[i][2])
    
    os.system('python makeShapeCardsNew.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight_legacy.txt "Hreco_dnn_prediction" "['+str(bin_ranges[i][0])+','+str(bin_ranges[i][1])+']" --unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_090120_091019_v6_skim2lss_forCP/2016/ --FMCs /nfs/user/atalier/skim_3l_cp_new/ --FMCs {P}/0_jmeUnc_v1 --FDs {P}/1_recl --FMCs {P}/1_recl_allvars --FMCs {P}/2_btag_SFs --FMCs {P}/2_scalefactors_lep_fixed --FMCs {P}/3_tauCount --Fs {P}/4_evtVars --FMCs {P}/5_BDThtt_reco_new_blah --Fs {P}/6_mva2lss --Fs {P}/6_mva3l --Fs {P}/6_mva4l  --xf TTTW --xf TTWH --tree NanoAOD --s2v -j 16 -l 35.9 -f --WA prescaleFromSkim --split-factor=-1  --od cards/kk  -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METFixEE2017.txt --plotgroup data_fakes+=.*_promptsub --neg   --threshold 0.01 --asimov signal --filter ttH-multilepton/filter-processes.txt  -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)" --binname ttH_3l_'+str(bin_ranges[i][2])+'_check --year 2016')
