from dataclasses import dataclass
@dataclass(frozen=True)

class Config:
    # Connectome generation
    n_rois: int = 100
    seed: int = 10
    data_dir: str = "~/nilearn_data"
    scaling_factor: float = 10.0          
    noise_loc: float = 0.1
    noise_scale: float = 0.05
    d0_range: tuple = tuple(range(0, 20))
    threshold_percent: float = 60

    # Kuramoto
    dt: float = 0.01
    eta: float = 5e-4
    w_min: float = 0.05
    time_steps: int = 1000
    record_every: int = 100

    # Coupling Constant Sweep
    sigma: float = 5.24
    k_max_factor: float = 5.0
    n_k: int = 25