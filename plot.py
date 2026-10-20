import numpy as np
import matplotlib.pyplot as plt
from nilearn.plotting import plot_matrix


class ConnectomePlotter:
    def __init__(self, region_labels=None, show_labels=False, cmap="magma", vmin=0, vmax = 1):
        self.region_labels = region_labels if show_labels else None
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax


    def plot_comparison(self, axes_row, W_0, result, K):
            plot_matrix(np.asarray(W_0, dtype=float), labels=self.region_labels,
                    axes=axes_row[0], vmax=self.vmax, vmin=self.vmin,
                    title="Unpruned Connectome", cmap=self.cmap, colorbar=False)
            plot_matrix(np.asarray(result, dtype=float), labels=None,
                        axes=axes_row[1], vmax=self.vmax, vmin=self.vmin,
                        title=f"Coupling Constant Value = {K:.3f}", cmap=self.cmap)

    def plot_sweep(self, W0, Results, K_values, save_path="Comparison_Kvals.png",
        row_indices=None, dpi=100):
        if row_indices is None:
            row_indices = range(len(K_values))
        row_indices = list(row_indices)
        n_rows = len(row_indices)
        fig, axes = plt.subplots(nrows=n_rows, ncols=2,
                                figsize=(12, 4 * n_rows), squeeze=False)
        for row, idx in zip(axes, row_indices):
            self.plot_comparison(row, W0, Results[idx], K_values[idx])
        plt.tight_layout()
        fig.savefig(save_path, dpi=dpi)
        plt.close(fig)
        return save_path

