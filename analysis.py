import numpy as np
import bct
import matplotlib.pyplot as plt
import pandas as pd
from nilearn import datasets
from sklearn.utils import Bunch
from config import Config
from master import main
from generating_connectomes import Connectome_Generator


class Analysis:
    def __init__(self, generator : Connectome_Generator = Connectome_Generator(), cfg: Config = Config()):
        self.config = cfg
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

    def Compare_ASD(self):
        abide = datasets.fetch_abide_pcp(
            n_subjects = 5,
            pipeline="cpac",
            derivatives=["func_preproc"],
            quality_checked=True,
                )
        pheno = pd.DataFrame(abide.phenotypic)
        select = pheno[
            (pheno["DX_GROUP"] == 1)
            & (pheno["AGE_AT_SCAN"] < 25)
            & (pheno["FILE_ID"] != "no_filename")
        ]
        n_subjects_selected = select.shape[0] 
        n_subjects = 1
        idx = select.index[:n_subjects]
        asd_dataset = Bunch(
            func=[abide.func_preproc[i] for i in idx],
            confounds=[None] * len(idx),   
        )
        self.load_atlas()          
        self.euclidean_dist()      
        self.reference_metreics(dataset=asd_dataset)
        print("L_ref:", self.L_ref)
        print("C_ref:", self.C_ref)
        print("D_ref:", self.D_ref)
        print("Number of Connectomes in average", n_subjects_selected)

    def results_graph_metrics(self):
        self.results_graph_metrics = []
        for result in self.results:
            self.results_graph_metrics.append(self.graph_metrics())


    def compare_rmsd(self):
        self.results_graph_metrics()
        L = [item[0] for item in self.results_graph_metrics]
        C = [item[1] for item in self.results_graph_metrics]
        D = [item[2] for item in self.results_graph_metrics]

        if self.config.compare_asd:
            self.Compare_ASD()

            RMSD_asd = np.sqrt((L - self.L_ref)**2 + (C - self.C_ref)**2 + (D - self.D_ref)**2)

        if self.config.compare_nt:
            pass
        if self.config.compare_sz:
            pass







               


analyser = Analysis()
analyser.Compare_ASD()


 

