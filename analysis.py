import numpy as np
import bct
import matplotlib.pyplot as plt
from kuramoto import run_kuramoto
from Coupling_constant import K_c


## Testing if its random 

origional_connectome = np.load('origional_connectome.npy')
Results = np.load('Results.npy', allow_pickle=True)

n_null = 3 # Number of random networks
null_connectomes = []

for i in range(n_null):
    W, _ = bct.randmio_und(origional_connectome.copy(), itr=10) # itr is like this number of rand rewireings per edge
    null_connectomes.append(W) # Rewire randomly 


K_crit = K_c()
K_values = np.arange(0, 2 * K_crit, 1)


null_results = {} # store as dict
z_scores = []

for i, K in enumerate(K_values):
    null_results[K] = []

    for W in null_connectomes:
        pruned = run_kuramoto(K, W)[-1]
        null_results[K].append(pruned)

    results_cluster_mean = np.mean(bct.clustering_coef_wu(Results[i]))
    null_clusters = [np.mean(bct.clustering_coef_wu(W_res)) for W_res in null_results[K]]

    null_cluster_mean = np.mean(null_clusters)
    null_cluster_std = np.std(null_clusters)

    print(K, results_cluster_mean, null_clusters,
      "| min real:", Results[i].min(),
      "| min nulls:", [w.min() for w in null_results[K]])

    if np.abs(null_cluster_std) > 0:
        z = (results_cluster_mean - null_cluster_mean) / null_cluster_std
    else:
        z = np.nan
    z_scores.append(z)

print("z_scores:", z_scores)
fig, axes = plt.subplots(nrows=1, ncols=1, figsize= (16, 8))
axes.plot(K_values, z_scores, marker = 'o')
axes.axhline(0)
plt.savefig('RealvsNull')

