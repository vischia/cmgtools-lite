from ROOT import *
import numpy as np

import h5py
from keras import optimizers
from keras.models import load_model
import tensorflow as tf

f = TFile("INPUT_FILE", "update")
from array import array

dnn_score = array( 'f', [-1.0] )
tree = f.Get('Friends')
newbranch = tree.Branch('dnn_prediction', dnn_score, 'dnn_prediction/F')

def loss_MSEDeltaVar(y_true, y_pred):
    y_true = tf.cast(y_true,tf.float32)
    y_pred = tf.cast(y_pred,tf.float32)
    y_true_mean = tf.reduce_mean(y_true)
    y_pred_mean = tf.reduce_mean(y_pred)
    base = tf.reduce_mean((y_true-y_pred)**2)
    var_true = tf.reduce_mean((y_true-y_true_mean)**2)
    var_pred = tf.reduce_mean((y_pred-y_pred_mean)**2)
    var_diff = abs(var_true - var_pred)
    val = base*var_diff
    return val


model_dnn = load_model('dnn_trained.h5', custom_objects={'loss_MSEDeltaVar': loss_MSEDeltaVar})

for entry in tree:

    dnn_score[0] = (float(model_dnn.predict(np.transpose(np.array([[entry.Hreco_Lep0_pt], [entry.Hreco_Lep0_eta], [entry.Hreco_Lep0_phi], [entry.Hreco_Lep1_pt], [entry.Hreco_Lep1_eta], [entry.Hreco_Lep1_phi], [entry.Hreco_HadTop_pt], [entry.Hreco_HadTop_eta], [entry.Hreco_HadTop_phi], [entry.Hreco_TopScore], [entry.Hreco_met], [entry.Hreco_Jets_plus_Lep_pt], [entry.Hreco_Jets_plus_Lep_eta], [entry.Hreco_Jets_plus_Lep_phi], [entry.Hreco_More5_Jets_pt], [entry.Hreco_More5_Jets_eta], [entry.Hreco_More5_Jets_phi], [entry.Hreco_All5_Jets_pt], [entry.Hreco_All5_Jets_eta], [entry.Hreco_All5_Jets_phi], [entry.Hreco_met_phi] ] )))))
    newbranch.Fill()

f.Write()
f.Close()
