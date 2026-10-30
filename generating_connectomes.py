import numpy as np
from nilearn import datasets, plotting
from scipy.spatial.distance import cdist
import bct
import os
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from config import Config


class Connectome_Generator:
    def __init__(self, cfg: Config = Config()):
        self.cgf = cfg
        self.data_dir = os.path.expanduser(cfg.data_dir)
        self.atlas = None
        self.map_filepath = None
        self.region_labels = None
        self.roi_coordinates = None
        self.distance_matrix = None
        self.L_ref = self.C_ref = self.D_ref = None
        self.d0_best = None
        self.W = None

    def load_atlas(self):
        self.atlas = datasets.fetch_atlas_schaefer_2018(n_rois = self.cgf.n_rois, data_dir=self.data_dir)
        self.map_filepath = self.atlas.maps
        self.region_labels = self.atlas.labels
        self.roi_coordinates= plotting.find_parcellation_cut_coords(self.map_filepath)
        self.region_labels = self.region_labels[1::]

    def euclidean_dist(self):
        self.distance_matrix = cdist(self.roi_coordinates, self.roi_coordinates, metric='euclidean')
        return self.distance_matrix    

    # Below Means you can call this function without creating an instance of the class
    # so like turns it into a normal fn
    @staticmethod
    def graph_metrics(bin_matrix):
        path_dist = bct.distance_bin(bin_matrix)
        L, _, _, _, _ = bct.charpath(path_dist)
        C = np.mean(bct.clustering_coef_bu(bin_matrix))
        D = np.mean(bin_matrix > 0)
        return L, C, D

    def connection_probability(self, d_0):
        if d_0 <= 0:
            return np.zeros_like(self.distance_matrix)
  
        return self.cgf.scaling_factor * np.exp(- self.distance_matrix / d_0)

    def noise_symmetric(self, d_0, rng): 
        P_mat = self.connection_probability(d_0)  
        noise = rng.normal(loc= self.cgf.noise_loc, scale=self.cgf.noise_scale, size=P_mat.shape) 
        noisey_P = P_mat + noise
        W = (noisey_P + noisey_P.T) / 2
        np.fill_diagonal(W, 0)
        return W

    @staticmethod
    def reference_metreics(self, dataset=None):
        if dataset == None:
            dataset = datasets.fetch_development_fmri(n_subjects = 1, age_group = 'child', data_dir=self.data_dir)
        masker = NiftiLabelsMasker(labels_img=self.map_filepath, 
                       standardize='zscore_sample', 
                       memory='nilearn_cache')
        cluster_all, path_length_all, density_all = [], [], []
        for fmri_file, confounds_file in zip(dataset.func, dataset.confounds):
            time_series = masker.fit_transform(fmri_file, confounds= confounds_file)
            correlation_measure = ConnectivityMeasure(kind = 'correlation')  
            matrix = correlation_measure.fit_transform([time_series])[0]
            np.fill_diagonal(matrix, 0)
            matrix[matrix < 0] = 0 
            bct.binarize(matrix, copy = False)
            L, C, D = self.graph_metrics(matrix)
            path_length_all.append(L)
            cluster_all.append(C)
            density_all.append(D)
        self.L_ref = np.mean(path_length_all)
        self. C_ref = np.mean(cluster_all)
        self.D_ref = np.mean(density_all)


    def d_0_Sweep(self, rng):

        RMSD = np.inf
        d_0_best = 0

        for d_0 in self.cgf.d0_range:

            W = self.noise_symmetric(d_0, rng)
            threshold = np.percentile(W[W > 0], self.cgf.threshold_percent) 
            W_bin = (W >= threshold).astype(int)

            L, C, D = self.graph_metrics(W_bin)

            RMSD_now = np.sqrt((C - self.C_ref)**2 + (L - self.L_ref)**2 + (D - self.D_ref)**2)

            if RMSD_now < RMSD:
                RMSD = RMSD_now
                d_0_best = d_0

        self.d0_best = d_0_best


    def create_matrix(self, rng):
        W = self.noise_symmetric(self.d0_best, rng)
        return np.clip(W, 0, 1)

    def generate_connectome(self):
        rng = np.random.RandomState(self.cgf.seed)
        self.load_atlas()
        self.euclidean_dist()
        self.reference_metreics()
        self.d_0_Sweep(rng)
        self.W = self.create_matrix(rng)
        return self.W
