import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting
from nilearn.plotting import plot_connectome, plot_matrix, show, view_connectome
from generating_connectomes import initialising_atlas
from Coupling_constant import Coupling_constant

K_values = Coupling_constant()
atlas, map_filepath, region_labels, roi_coordinates = initialising_atlas()

Results = np.load('Results.npy', allow_pickle=True)
origional_connectome = np.load('origional_connectome.npy')
origional_connectome = np.asarray(origional_connectome, dtype=float)

n_rows = len(K_values)
i_iterates = range(n_rows)

fig, axes = plt.subplots(nrows=n_rows, ncols=2, figsize= (12, 4 * n_rows))

def plot_connectome_matrix(K, result, i):
    result = np.asarray(result , dtype=float)


    plot_matrix(
        result,
        labels= None,
        axes = axes[i, 1],
        vmax=1,
        vmin=0,
        title= f"Coupling Constant Value = {K}",
        cmap= 'magma',
        )

    plot_matrix(
        origional_connectome,
        labels= region_labels,
        axes = axes[i,0],
        vmax=1,
        vmin=0,
        title="Unpruned Connectome",
        cmap= 'magma',
        )
    
    return 


def plotting_loop():
    for K, result, i in zip(K_values, Results, i_iterates):

        plot_connectome_matrix(K, result, i)

    plt.tight_layout()
    plt.savefig('Comparison_Kvals')

plotting_loop()





