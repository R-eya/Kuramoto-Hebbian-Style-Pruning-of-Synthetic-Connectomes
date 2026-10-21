import numpy as np
from dataclasses import dataclass
@dataclass(frozen=True)

class Config:
    # Connectome generation
    n_rois: int = 100
    seed: int = 10
    data_dir: str = "~/nilearn_data"
    scaling_factor: float = 10.0        
    noise_loc: float = 0.05
    noise_scale: float = 0.05
    d0_range: tuple = tuple(range(0, 20))
    threshold_percent: float = 60

    # Kuramoto
    dt: float = 0.01
    eta: float = 5e-4
    time_steps: int = 2000 # ~1000 steps is 1 year
    w_min: float = 0.1
    record_each: int = 100
    sync_reward: float = 0.5
    desync_penalty: float = 1

    # Intrinsic Frequency 
    alpha_max: float = 12.0
    alpha_min: float = 8.0
    node_strength_proportion: float = 0.5 # between 0 and 1
    physical_distance_proportion: float = 1 - node_strength_proportion

    # Coupling Constant Sweep
    sigma: float = (alpha_max - alpha_min)*2*np.pi / np.sqrt(alpha_max)
    k_max_factor: float = 15.0
    number_of_k_values: int = 25