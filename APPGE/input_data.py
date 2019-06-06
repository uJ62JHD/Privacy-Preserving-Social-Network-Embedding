import pickle as pkl
import scipy.sparse as sp
import tensorflow as tf
import numpy as np



def load_data(dataset):
    
    with open('../data/{}_feats.pkl'.format(dataset), 'rb') as f1:
        features = pkl.load(f1)
    with open('../data/{}_adj.pkl'.format(dataset), 'rb') as f2:
        adj = pkl.load(f2,encoding='latin1')
    
    val_edges = np.load('../data/{}_val_edges.npy'.format(dataset))
    val_edges_false = np.load('../data/{}_val_edges_false.npy'.format(dataset))
    test_edges = np.load('../data/{}_test_edges.npy'.format(dataset))
    test_edges_false = np.load('../data/{}_test_edges_false.npy'.format(dataset))

    with open('../data/{}_adj_train.pkl'.format(dataset), 'rb') as handle:
        adj_train = pkl.load(handle)
        
    return adj, features,adj_train, val_edges, val_edges_false, test_edges, test_edges_false