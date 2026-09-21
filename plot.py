import numpy as np
from nilearn import datasets, plotting
from generating_connectomes import initialising_atlas
import matplotlib.pyplot as plt

atlas, map_filepath, region_labels, roi_coordinates = initialising_atlas()
connectomes = np.load('pruned_weights.npy', allow_pickle=True)
connectome = np.load('origional_connectome.npy')

from nilearn.plotting import (
    plot_connectome,
    plot_matrix,
    show,
    view_connectome,
)

def plot_connectome_matrix(connectome):
    plot_matrix(
        connectome, #np.array(connectomes[0], dtype=float),
        labels= region_labels,
        figure=(16, 9),
        vmax=1,
        vmin=0,
        title="Connectomes Mat",
        cmap= 'magma',
        )
    plt.savefig
    return 

plot_connectome_matrix(connectome)
plt.savefig('mat_plot')