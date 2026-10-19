import numpy as np


def K_values(W, sigma = 5.24):
    """
    Returns K values and theoreical critical threshold value of K.
    """
    lam = np.max(np.linalg.eigvalsh(W)) 
    K_c = sigma * np.sqrt(8 / np.pi) / lam
    K_values = np.linspace(0, 5 * K_c, 25)
    return K_values, K_c
