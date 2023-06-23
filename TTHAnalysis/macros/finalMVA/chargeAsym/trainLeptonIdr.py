import os 
import torch 
import uproot
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np 
import json 

class ttwdataset( Dataset ):
    def __init__(self, path):
        self.path=path
        if not os.path.isfile(f'{self.path}/tensor.p'):
            self.produce()

        self.features, self.labels=torch.load(f'{self.path}/tensor.p')
        with open(f'{self.path}/features_names.json') as f:
            self.features_names = json.load( f )

    def __len__(self):
        return self.labels.shape[0]

    def __getitem__(self, indx): 
        return self.features[indx,:], self.labels[indx,:]

        
    def produce(self):
        datasets=[]
        for year in '2016,2016APV,2017,2018'.split(','):
            fullpath=f'{self.path}/{year}/A_ttWforlepton_v2/'
            for fil in os.listdir(fullpath):
                if not fil.endswith(".root"): continue
                tree = uproot.open(f'{fullpath}/{fil}' )['Friends']
                datasets.append( tree.arrays( tree.keys(), library='pd') )
        dataset = pd.concat( datasets ) 
        features_names = [x for x in dataset.columns]; features_names.remove('label')


        feature_tensor = torch.from_numpy( dataset[features_names].values )
        label_tensor   = torch.from_numpy( dataset[['label']].values )
        with open(f'{self.path}/features_names.json','w') as f:
            json.dump( features_names, f)
            
        
        torch.save((feature_tensor, label_tensor), f'{self.path}/tensor.p')


class Net(torch.nn.Module):
    def __init__(self, inputvars=6, device='cpu'):
        super().__init__()
        self.main_module = torch.nn.Sequential( 
            torch.nn.Linear(inputvars, 32),
            torch.nn.ReLU(True),
            torch.nn.Linear(32, 16),
            torch.nn.ReLU(True),
            torch.nn.Linear(16, 8),
            torch.nn.ReLU(True),
            torch.nn.Linear(8, 1 ),
            torch.nn.Sigmoid(),
        )
        self.main_module.to(device)
    def forward(self, x):
        return self.main_module(x)
            

def make_input_plots( train_features, train_labels, 
                      test_features, test_labels ):
    
    for feature in range( train_features.shape[1] ):
        train_top,bins,_=plt.hist((train_features[train_labels.flatten()==1])[:,feature] , label='Train. Lep from top', bins=50,histtype='step', density=True, color='tab:blue')
        train_w  ,_,_   =plt.hist((train_features[train_labels.flatten()==0])[:,feature] , label='Train. Lep from W',bins=bins,histtype='step', density=True, color='tab:orange')
        test_top ,_,_   =plt.hist((test_features[test_labels.flatten()==1])[:,feature] , label='Test. Lep from top',bins=bins, alpha=0.4, density=True, color='tab:blue')
        test_w   ,_,_   =plt.hist((test_features[test_labels.flatten()==0])[:,feature] , label='Test. Lep from W',bins=bins, alpha=0.4, density=True, color='tab:orange')
        plt.legend()
        plt.savefig(f"models/input_{feature}.png")
        plt.clf()

    


def make_eval_plots( train_score, train_labels,
                     test_score, test_labels, epoch, name):
    train_top,bins,_=plt.hist(train_score[train_labels==1] , label='Train. Lep from top', bins=50,histtype='step', density=True, color='tab:blue')
    train_w  ,_,_   =plt.hist(train_score[train_labels==0] , label='Train. Lep from W',bins=bins,histtype='step', density=True, color='tab:orange')
    test_top ,_,_   =plt.hist(test_score[test_labels==1] , label='Test. Lep from top',bins=bins, alpha=0.4, density=True, color='tab:blue')
    test_w   ,_,_   =plt.hist(test_score[test_labels==0] , label='Test. Lep from W',bins=bins, alpha=0.4, density=True, color='tab:orange')
    plt.legend()
    plt.savefig(f"{name}/score_{epoch}.png")
    plt.clf()

    for i,(top,w) in enumerate([[train_top, train_w],[test_top,test_w]]):
        cum_top = np.cumsum( top ) ; cum_top /= np.max(cum_top) 
        cum_w   = np.cumsum( w )   ; cum_w   /= np.max(cum_w  )
        plt.plot( cum_top, cum_w, label='Test' if i else 'Train')
    plt.legend()
    plt.savefig(f'{name}/roc_{epoch}.png')
    plt.clf()
        

    

    

if __name__=="__main__":


    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--epochs",type=int, default=500, help="Number of epochs to train the net");
    parser.add_argument("--no-cuda", dest="cuda", action='store_false', default=True, help="Do not try to use cuda. Otherwise it will try to use cuda only if its available");
    parser.add_argument("--cuda-index", type=int, default=0, help="Index of the device to use");
    parser.add_argument("--learning-rate", type=float, default=0.00000005, help="Optimizer learning rate")
    parser.add_argument("--optimizer", type=str, default='SGD', help="Optimizer to be used")
    parser.add_argument("--momentum", type=float, default=0.9, help="Optimizer momentum")
    parser.add_argument("--model-prefix",type=str, default="model", help="Prefix for the name");
    parser.add_argument("--batch-size",type=int, default=64, help="Minibatch size");
    parser.add_argument("--path",type=str, default="/pnfs/psi.ch/cms/trivcat/store/user/sesanche//NanoTrees_UL_v2_060422_newfts_skim2lss/", help="Path where to take the data from");
    args = parser.parse_args()

    # Decide if we will (if we can) use the GPU
    cuda = args.cuda and torch.cuda.is_available()
    if not torch.cuda.is_available() and args.cuda:
        print("Warning, you tried to use cuda, but its not available. Will use the CPU")
    if cuda:
        cuda_index=args.cuda_index
    else:
        cuda_index='cpu'
        torch.set_num_threads(8)


    dataset = ttwdataset(args.path)
    net = Net(7, cuda_index)

    training,test  = torch.utils.data.random_split( dataset, [0.7, 0.3], generator=torch.Generator().manual_seed(42))
    dataloader     = DataLoader(  training  , batch_size=args.batch_size, shuffle=True)
    if args.optimizer in ['SGD','RMSprop']:
        optimizer      = getattr(torch.optim, args.optimizer)(net.parameters(), lr=args.learning_rate, momentum=args.momentum)
    elif args.optimizer == 'Adam':
        optimizer      = getattr(torch.optim, args.optimizer)(net.parameters(), lr=args.learning_rate, betas=(args.momentum,args.momentum*1.11))
    else:
        raise RuntimeError("Optimizer not defined")

    test_features,test_labels = test[:]
    train_features,train_labels = training[:]
    # make_input_plots( train_features, train_labels, 
    #                   test_features, test_labels ) 
                      
    name = f"{args.model_prefix}_batch_{args.batch_size}_lr_{args.learning_rate}_optim_{args.optimizer}_momentum_{args.momentum}"
    if not os.path.exists(name):
        os.makedirs(name)

    cost =  torch.nn.BCELoss( reduction='mean')

    losses_train=[]; losses_test=[]

    for epoch in range(args.epochs):
        loop=tqdm( enumerate(dataloader))
        sum_loss=0
        for i,(features,labels) in loop:
            optimizer.zero_grad()
            loss = cost( net(features).flatten(), labels.flatten())
            loss.backward()
            optimizer.step()
            
            sum_loss+=loss.item()
            if i%100 == 0:
                if i > 0:
                    loop.set_description(f"Epoch {epoch}, cost {sum_loss/i}")

        loss_test = cost( net(test_features), test_labels).item()
        loss_train = cost( net(train_features), train_labels).item()

        losses_train.append(loss_train); losses_test.append(loss_test)
        print(f"Test loss {loss_test}, train loss {loss_train}")

        if epoch%20==0 or epoch==args.epochs-1:
            torch.save(net, f'{name}/network_{epoch}.pth')

            # Plot the cost function
            plt.plot( range(epoch+1), losses_test, label='Test')
            plt.plot( range(epoch+1), losses_train, label='Train')
            plt.savefig(f'{name}/cost_{epoch}.png')
            plt.clf()

            make_eval_plots( net(train_features).detach().numpy(), train_labels.detach().numpy(),
                             net(test_features).detach().numpy() , test_labels.detach().numpy(),
                             epoch, name
            )
