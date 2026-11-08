import numpy as np
import bct
import matplotlib.pyplot as plt
import pandas as pd
import openneuro as on
from nilearn import datasets
from sklearn.utils import Bunch
from config import Config
from master import main
from generating_connectomes import Connectome_Generator
from Coupling_constant import K_values


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
        plt.figure()
        #k_min, k_max = np.min(self.K_vals), np.max(self.K_vals)
        #L_0, C_0, D_0 = self.graph_metrics(self.W_0)
        #plt.plot([k_min, k_max], [L_0, L_0], color='red', label='Mean Path Length')
        #plt.plot([k_min, k_max], [C_0, C_0], color='green', label='Mean Clustering Co-efficient')
        #plt.plot([k_min, k_max], [D_0, D_0], color='blue', label='Network Density')

        self.metrics_of_results()

        plt.plot(self.K_vals, self.path_length_res, color='red', label='Mean Path Length')
        plt.plot(self.K_vals, self.cluster_res, color='green', label='Mean Clustering Co-efficient')
        plt.plot(self.K_vals, self.density_res, color='blue', label='Network Density')
        plt.plot(self.K_c, color = 'black', linestyle = '-')   

        plt.axvline(self.K_c, color='black', linestyle=':', label=f'K_c = {self.K_c:.3f}')

        plt.xlabel('K Value')
        plt.ylabel('Change in Metric')
        plt.legend(loc='upper right')
        plt.savefig('./Results/Graph_Metrics.png', dpi=200, bbox_inches='tight')
        plt.close()

    def Compare_ASD(self):
        """
        Fetches ASD connectomes from ABIDE dataset.
        Calculates the mean graph metrics.
        """
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
        self.n_subjects_selected_asd = select.shape[0] 
        n_subjects = 1
        idx = select.index[:n_subjects]
        asd_dataset = Bunch(
            func=[abide.func_preproc[i] for i in idx],
            confounds=[None] * len(idx),   
        )
      
        self.reference_metrics(dataset=asd_dataset)


    def Compare_NT(self):
        abide = datasets.fetch_abide_pcp(
        n_subjects = 5,
        pipeline="cpac",
        derivatives=["func_preproc"],
        quality_checked=True,
                )
        pheno = pd.DataFrame(abide.phenotypic)
        select = pheno[
            (pheno["DX_GROUP"] == 0)
            & (pheno["AGE_AT_SCAN"] < 25)
            & (pheno["FILE_ID"] != "no_filename")
        ]
        self.n_subjects_selected_nt = select.shape[0] 
        n_subjects = 1
        idx = select.index[:n_subjects]
        nt_dataset = Bunch(
            func=[abide.func_preproc[i] for i in idx],
            confounds=[None] * len(idx),   
        )
      
        self.reference_metrics(dataset=nt_dataset)

    def Compare_sz(self):
        raise NotImplementedError
        url = "https://openneuro.org"
        try:
            df = pd.read_csv(url, sep='\t')
        except Exception:
            url = "https://openneuro.org"
            df = pd.read_csv(url, sep='\t')

        select = df[
        (df['age'] < 25) & 
        (df['Group'].str.lower().str.contains('schizophrenia', na=False))
        ]
        target = select['participant_id'].to_list()[:5] # First 5 participants
        include = [f"derivatives/fmriprep/{sub}/func/*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz" for sub in target]

        if len(include) > 0:
        
            tcp = on.download(
                dataset="ds005237",
                target_dir="./tcp_filtered_young_sz",
                include=include
            )
        else:
            raise Exception("Nothing included in dataset")

        self.reference_metrics(dataset=tcp)
        
        

    def results_graph_metrics(self):
        self.results_graph_metrics_ = []
        for result in self.results:
            self.results_graph_metrics_.append(self.graph_metrics(result))


    def compare_rmsd(self):
        """
        Calculates RMSD between reference connectomes and results (over K range).
        """
        self.load_atlas()          
        self.euclidean_dist()
        self.results_graph_metrics()
        L = np.array([item[0] for item in self.results_graph_metrics_])
        C = np.array([item[1] for item in self.results_graph_metrics_])
        D = np.array([item[2] for item in self.results_graph_metrics_])

        if self.config.compare_asd:
            self.Compare_ASD()

            self.RMSD_asd = np.sqrt(((L - self.L_ref)/ self.L_ref )**2 + ((C - self.C_ref)/ self.C_ref)**2 + ((D - self.D_ref)/ self.D_ref)**2)**0.5

        if self.config.compare_nt:
            self.Compare_NT()
            self.RMSD_nt = np.sqrt(((L - self.L_ref)/ self.L_ref )**2 + ((C - self.C_ref)/ self.C_ref)**2 + ((D - self.D_ref)/ self.D_ref)**2)**0.5

        if self.config.compare_sz:
            raise NotImplementedError


    def Plot_RMSD_Comparison(self):
        self.compare_rmsd()
        if self.config.compare_asd:
            plt.figure()
            plt.plot(self.K_vals, self.RMSD_asd, color='red', label = f"RMSD of results to average of {self.n_subjects_selected_asd} ASD Connectomes")
            plt.xlabel("K value")
            plt.ylabel("RMSD")
            plt.legend()
            plt.savefig('./Results/RMSD_ASD.png')

        if self.config.compare_nt:
            plt.figure()
            plt.plot(self.K_vals, self.RMSD_nt, color='blue', label = f"RMSD of results to average of {self.n_subjects_selected_nt} NT Connectomes")
            plt.xlabel("K value")
            plt.ylabel("RMSD")
            plt.legend()
            plt.savefig('./Results/RMSD_NT.png')
        if self.config.compare_sz:
            pass



if __name__ == "__main__":
    analyser = Analysis()
    analyser.Plot_RMSD_Comparison()
    analyser.plot_metric_change()


 

