
#fake_rates_to_add=["jer%d"%i for i in range(6)]
fake_rates_to_add=["jesHEMIssue","jesAbsolute","jesAbsolute_year","jesBBEC1","jesBBEC1_year","jesEC2","jesEC2_year","jesFlavorQCD","jesHF","jesHF_year","jesRelativeBal","jesRelativeSample_year"]




for side in ["Up","Down"]:
    for fr in fake_rates_to_add:
        template = open("fr-template.txt").read()
        out=template.replace("template",fr+side)
        outf=open("fr-%s.txt"%(fr+side),'w')
        outf.write(out)
        outf.close()
