import torch
from glob import glob
from trainLeptonIdr import ttwdataset, Net
import matplotlib.pyplot as plt
import os

dataset = ttwdataset("/pnfs/psi.ch/cms/trivcat/store/user/sesanche//NanoTrees_UL_v2_060422_newfts_skim2lss/")
test_features,test_labels = dataset[:]
top_leptons=test_features[test_labels.flatten()==1]
w_leptons=test_features[test_labels.flatten()==0]

for model in glob("model_v2_*optim*"):
    #print(model,f'{model}/network_499.pth')
    if not os.path.isfile(f'{model}/network_499.pth'):
        print(f"no file {model}/network_499.pth")
        continue
    net = torch.load(f'{model}/network_499.pth')
    per_event_score=net(top_leptons)-net(w_leptons)
    score = torch.sum(per_event_score>0).item()/ per_event_score.shape[0]
    if score > 0.69:
        print(model, score)

#plt.hist(per_event_score.detach().numpy(), bins=200, density=True, color='tab:blue')
#plt.savefig("per_event_score.png")
