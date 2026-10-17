import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting
from nilearn.plotting import plot_connectome, plot_matrix, show, view_connectome
from generating_connectomes import initialising_atlas



def plot_connectome_matrix(K, synthetic_origional, result, i, axes, param_tuple):
    result = np.asarray(result , dtype=float)
    atlas, map_filepath, region_labels, roi_coordinates = param_tuple


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
        synthetic_origional,
        labels= region_labels,
        axes = axes[i,0],
        vmax=1,
        vmin=0,
        title="Unpruned Connectome",
        cmap= 'magma',
        )
    
    return 


def plotting_loop(Results, synthetic_origional, K_values_list):
    """
    Plots origional synthetic connectome vs kuromoto'd connectome for each of the k values
    """

    atlas, map_filepath, region_labels, roi_coordinates = initialising_atlas()
    param_tuple = (atlas, map_filepath, region_labels, roi_coordinates)
    n_rows = len(K_values_list)
    i_iterates = range(n_rows)
    fig, axes = plt.subplots(nrows=n_rows, ncols=2, figsize= (12, 4 * n_rows))

    for K, result, i in zip(K_values_list, Results, i_iterates):

        plot_connectome_matrix(K, synthetic_origional, result, i, axes, param_tuple=param_tuple)

    plt.tight_layout()
    plt.savefig('Comparison_Kvals')







