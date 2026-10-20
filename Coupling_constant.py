import numpy as np
from config import Config

def K_values(W, cfg: Config = Config()):
    """
    Returns K values and theoreical critical threshold value of K.
    """
    lam = np.max(np.linalg.eigvalsh(W)) 
    K_c = cfg.sigma * np.sqrt(8 / np.pi) / lam
    K_values = np.linspace(0, cfg.k_max_factor * K_c, cfg.number_of_k_values)
    return K_values, K_c
