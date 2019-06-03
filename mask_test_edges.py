import pickle as pkl
import scipy.sparse as sp
import numpy as np
# build test set with 10% positive links
# NOTE: Splits are randomized and results might slightly deviate from reported numbers in the paper.
# TODO: Clean up.
def sparse_to_tuple(sparse_mx):
    if not sp.isspmatrix_coo(sparse_mx):
        sparse_mx = sparse_mx.tocoo()
    coords = np.vstack((sparse_mx.row, sparse_mx.col)).transpose()
    values = sparse_mx.data
    shape = sparse_mx.shape
    return coords, values, shape


with open('./data/yale_adj.pkl', 'rb') as f2:
    adj = pkl.load(f2,encoding='latin1')

# Remove diagonal elements
adj = adj - sp.dia_matrix((adj.diagonal()[np.newaxis, :], [0]), shape=adj.shape)
adj.eliminate_zeros()
# Check that diag is zero:
assert np.diag(adj.todense()).sum() == 0

adj_triu = sp.triu(adj)
adj_tuple = sparse_to_tuple(adj_triu)
edges = adj_tuple[0]
edges_all = sparse_to_tuple(adj)[0]
num_test = int(np.floor(edges.shape[0] / 10.))
num_val = int(np.floor(edges.shape[0] / 20.))

all_edge_idx = list(range(edges.shape[0]))
np.random.shuffle(all_edge_idx)
val_edge_idx = all_edge_idx[:num_val]
test_edge_idx = all_edge_idx[num_val:(num_val + num_test)]
test_edges = edges[test_edge_idx]
val_edges = edges[val_edge_idx]
train_edges = np.delete(edges, np.hstack([test_edge_idx, val_edge_idx]), axis=0)

def ismember(a, b, tol=5):
    rows_close = np.all(np.round(a - b[:, None], tol) == 0, axis=-1)
    return np.any(rows_close)

test_edges_false = []
while len(test_edges_false) < len(test_edges):
    idx_i = np.random.randint(0, adj.shape[0])
    idx_j = np.random.randint(0, adj.shape[0])
    if idx_i == idx_j:
        continue
    if ismember([idx_i, idx_j], edges_all):
        continue
    if test_edges_false:
        if ismember([idx_j, idx_i], np.array(test_edges_false)):
            continue
        if ismember([idx_i, idx_j], np.array(test_edges_false)):
            continue
    test_edges_false.append([idx_i, idx_j])

val_edges_false = []
while len(val_edges_false) < len(val_edges):
    idx_i = np.random.randint(0, adj.shape[0])
    idx_j = np.random.randint(0, adj.shape[0])
    if idx_i == idx_j:
        continue
    if ismember([idx_i, idx_j], train_edges):
        continue
    if ismember([idx_j, idx_i], train_edges):
        continue
    if ismember([idx_i, idx_j], val_edges):
        continue
    if ismember([idx_j, idx_i], val_edges):
        continue
    if val_edges_false:
        if ismember([idx_j, idx_i], np.array(val_edges_false)):
            continue
        if ismember([idx_i, idx_j], np.array(val_edges_false)):
            continue
    val_edges_false.append([idx_i, idx_j])



data = np.ones(train_edges.shape[0])

# Re-build adj matrix
adj_train = sp.csr_matrix((data, (train_edges[:, 0], train_edges[:, 1])), shape=adj.shape)
adj_train = adj_train + adj_train.T



np.save('yale_test_edges.npy',test_edges)
np.save('yale_val_edges.npy',val_edges)
np.save('yale_test_edges_false.npy',test_edges_false)
np.save('yale_val_edges_false.npy',val_edges_false)

with open('yale_adj_train.pkl', 'wb') as f2:
    adj = pkl.dump(adj_train,f2)

