## Config Decisions 
 
 # Connectome generation 
    scaling_factor: float = 10.0        
    threshold_percent: float = 60

  # Kuramoto 
    dt: float = 0.01
    eta: float = 5e-4
    w_min: float = 0.1
    time_steps: int = 1000 # ~1000 steps is 1 year
    record_each: int = 100
    sync_reward: float = 0.5
    desync_penalty: float = 1

  # Intrinsic Frequency Proportions 
    node_strength_proportion: float = 0.5 # between 0 and 1
    physical_distance_proportion: float = 1 - node_strength_proportion

  # Coupling Constant Sweep
    sigma: float = 5.24 # to put onto alpha freq scale
    k_max_factor: float = 10.0
    number_of_k_values: int = 25
