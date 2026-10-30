import numpy as np
import bct
import matplotlib.pyplot as plt
from ..config import Config
from ..master import main
from ..generating_connectomes import Connectome_Generator


class Analysis:
    def __init__(self, generator : Connectome_Generator = Connectome_Generator(), cfg: Config = Config()):
        self.W_0, self.K_vals, self.K_c, self.results = main()
        self.generator = generator
        self.path_length_res, self.cluster_res, self.density_res = [], [], []

    def __getattr__(self, attr):
        return getattr(self.generator, attr)

    def metrics_of_results(self):
        for result in self.results:
            bct.binarize(result, copy = False)
            L, C, D = self.graph_metrics(result)
            self.path_length_res.append(L)
            self.cluster_res.append(C)
            self.density_res.append(D)

    def plot_metric_change(self):
        k_min, k_max = np.min(self.K_vals), np.max(self.K_vals)
        L_0, C_0, D_0 = self.graph_metrics(self.W_0)
        plt.plot([k_min, k_max], [L_0, L_0], color='red', label='Mean Path Length')
        plt.plot([k_min, k_max], [C_0, C_0], color='green', label='Mean Clustering Co-efficient')
        plt.plot([k_min, k_max], [D_0, D_0], color='blue', label='Network Density')

        self.metrics_of_results()

        plt.plot(self.K_vals, self.path_length_res, color='red')
        plt.plot(self.K_vals, self.cluster_res, color='green')
        plt.plot(self.K_vals, self.density_res, color='blue')     

        plt.xlabel('K Values')

        plt.legend()
        plt.savefig('Graph_Metrics.png')

analyser = Analysis()
analyser.plot_metric_change()


 

