import numpy as np
import bct
import matplotlib.pyplot as plt
from kuramoto import run_kuramoto
from Coupling_constant import K_c
## Testing if a randomly connected network would give same result 

def cluster(W):
    """Get the mean of the clustering coeffiecient of a network, W"""
    return np.mean(bct.clustering_coef_wu(W))

def delta_C(K, W, seed):
    """Change in mean clustering coeffiecient after Kurumoto"""
    return cluster(run_kuramoto(K, W, seed=seed) - cluster(W))

np.random.seed(0)
origional_connectome = np.load('origional_connectome.npy')
base = bct.threshold_proportional(origional_connectome.copy(), 0.2)

n_null = 20 # Number of random networks
n_real_seeds = 20 # Compare to same number of real runs with diff seeds
null_connectomes = [bct.randmio_und(base.copy(), itr=10)[0] for _ in range(n_null)]


lam = np.max(np.linalg.eigvalsh(base))
K_crit = K_c()
K_values = np.arange(0, 2 * K_crit, 1)


null_results = {} # store as dict
z_scores = []

for K in K_values:
 
    real_final = run_kuramoto(K, base)[-1]
    real_cluster = np.mean(bct.clustering_coef_wu(real_final))

    # nulls, rewired
    null_clusters = []
    for W in null_connectomes:
        final = run_kuramoto(K, W)[-1]
        null_clusters.append(np.mean(bct.clustering_coef_wu(final)))

    real_delta = cluster(real_final) - cluster(base)
    null_deltas = [cluster(run_kuramoto(K, W)[-1]) - cluster(W) for W in null_connectomes]
    z = (real_delta - np.mean(null_deltas)) / np.std(null_deltas)
    z_scores.append(z)

print("z_scores:", z_scores)
fig, axes = plt.subplots(nrows=1, ncols=1, figsize= (16, 8))
axes.plot(K_values, z_scores, marker = 'o')
axes.axhline(0)
plt.savefig('RealvsNull')

