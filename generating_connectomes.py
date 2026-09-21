import numpy as np
from nilearn import datasets, plotting
from scipy.spatial.distance import cdist
import bct
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure


def euclidean_dist(coords):
    D = cdist(coords, coords, metric='euclidean')
    return D

def P(D, d_0):
    if d_0 <= 0:
        return np.zeros_like(D)
    scaling_factor = 10
    return scaling_factor * np.exp(- D / d_0)

def initialising_atlas():
    atlas = datasets.fetch_atlas_schaefer_2018(n_rois = 100, data_dir='/home/jane/nilearn_data')
    map_filepath = atlas.maps
    region_labels = atlas.labels
    roi_coordinates= plotting.find_parcellation_cut_coords(map_filepath)
    region_labels = region_labels[1::]
    return atlas, map_filepath, region_labels, roi_coordinates


def extract_reference_values():
    atlas, map_filepath, region_labels, roi_coordinates = initialising_atlas()
    region_labels = region_labels[1::]

    dataset = datasets.fetch_development_fmri(n_subjects = 1, age_group = 'child', data_dir='/home/jane/nilearn_data')
    masker = NiftiLabelsMasker(labels_img=map_filepath, 
                           standardize='zscore_sample', 
                           memory='nilearn_cache')


    cluster_all = []
    path_length_all = []
    density_all = []

    for i in range(1):
        fmri_file = dataset.func[i]
        confounds_file = dataset.confounds[i]

        time_series = masker.fit_transform(fmri_file, confounds= confounds_file)
        correlation_measure = ConnectivityMeasure(kind = 'correlation')  
        matrix = correlation_measure.fit_transform([time_series])[0]
        np.fill_diagonal(matrix, 0)
        matrix[matrix < 0] = 0 
        bct.binarize(matrix, copy = False)

        distance_matrix = bct.distance_bin(matrix)
        L_indiv, _, _, _, _ = bct.charpath(distance_matrix)
        C_indiv = np.mean(bct.clustering_coef_bu(matrix))

        path_length_all.append(L_indiv)
        cluster_all.append(C_indiv)
        density_all.append(np.mean(matrix > 0))

    L_ref = np.mean(path_length_all)
    C_ref = np.mean(cluster_all)
    D_ref = np.mean(density_all)

    return L_ref, C_ref, D_ref, euclidean_dist(roi_coordinates)

def determine_d_0(L_ref, C_ref, D_ref, distance_matrix):
    RMSD = np.inf
    d_0_best = 0
    D = distance_matrix



    for d_0 in range(0,20):

        P_mat = P(D, d_0)

        #np.random.seed(10) 
        noise = np.random.normal(loc=0.1, scale=0.05, size=P_mat.shape)
        W = P_mat + noise    

        W = (W + W.T) / 2
        np.fill_diagonal(W, 0)
        threshold = np.percentile(W[W > 0], 60)  # keep top 20%
        W = (W >= threshold).astype(int)

        distance_matrix = bct.distance_bin(W)
        L_indiv, _, _, _, _ = bct.charpath(distance_matrix)
        C_indiv = np.mean(bct.clustering_coef_bu(W))
        D_indiv = np.mean(W > 0)

        RMSD_now = np.sqrt((C_indiv - C_ref)**2 + (L_indiv - L_ref)**2 + (D_indiv - D_ref)**2)

        if RMSD_now < RMSD:
            RMSD = RMSD_now
            d_0_best = d_0

    return d_0_best


def getting_matrix(d_0_best, distance_matrix):
    np.random.seed(10)

    d_0 = d_0_best
    D = distance_matrix

    P_mat = P(D, d_0)  
    noise = np.random.normal(loc=0.1, scale=0.05, size=P_mat.shape)  # Is it bc noice can be negative and is too big??? - can be fixed move loc to like 0.5
    W = P_mat + noise
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)
    W = np.clip(W, 0, 1)

    return W




def generating_connectomes():
    L_ref, C_ref, D_ref, D = extract_reference_values()
    d_0_best = determine_d_0(L_ref=L_ref, C_ref=C_ref,D_ref=D_ref, distance_matrix= D)
    W =  getting_matrix(d_0_best=d_0_best, distance_matrix=D)
    np.save('origional_connectome.npy', W)
    print(d_0_best)
    #print(W)
    

generating_connectomes()