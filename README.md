## Model Decisions

### Kurmamoto Equation



### Coupling Constant
 $K_c = \sigma \sqrt{8 / \pi} / \lambda_{max}$
 






## Config Decisions 
 
 ### Connectome generation 
    scaling_factor: float = 10.0        
    threshold_percent: float = 60

  ### Kuramoto 
    dt: float = 0.01
    eta: float = 5e-4
    time_steps: int = 1000 | 1000 time-steps is approx 1 year between ages 1-2years
    w_min: float = 0.1
    record_each: int = 100 | for storage - to be used to show the dynamic pruning
    sync_reward: float = 0.5 | phase synchronisation is rewarded half as much as desynchronisation is    penalised to mitigate random hubs forming due to noise
    desync_penalty: float = 1

  ### Intrinsic Frequency Proportions 
    node_strength_proportion: float = 0.5 | The amount that the node strengths affect the intrinsic frequencies of each region i.e. hubs will have higher node strengths and therfore a stronger "pull" (intrinsic frequency).
    physical_distance_proportion: float = 1 - node_strength_proportion | The rest of the intrinsic frequency is determined by physical distance between regions

  ### Coupling Constant Sweep
    sigma: float = 5.24 | to put onto alpha freq scale
    k_max_factor: float = 10.0
    number_of_k_values: int = 25
