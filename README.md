## Model Decisions

### Kurmamoto Equation



### Coupling Constant
 $K_c = \sigma \sqrt{8 / \pi} / \lambda_{max}$
 






## Configureation Decisions
 
 <details>
 <summary>Connectome generation Parameters</summary>
  
 | Parameter | Value | Justification |
 | :--- | :--- | :--- |
 |scaling_factor| 10.0 | blank |      
 |threshold_percent | 60 | blank|

 </details>

  <details>
  <summary>Kuramoto Parameters</summary>
    
  | Parameter | Value | Justification |
  | :--- | :--- | :--- |
  |dt | 0.01 | |
  |eta| 5e-4 | |
  |time_steps| 1000 | 1000 time-steps is approx 1 year between ages 1-2years|
  |w_min| 0.1| |
  |record_each| 100 | for storage - to be used to show the dynamic pruning|
  |sync_reward| 0.5 | phase synchronisation is rewarded half as much as desynchronisation is    penalised to mitigate random hubs forming due to noise|
  |desync_penalty| 1| |

  </details>

   <details>
   <summary>Intrinsic Frequency Parameters</summary>
  
   | Parameter | Value | Justification |
   | :--- | :--- | :--- |
   |alpha_max| 12.0| |
   |alpha_min| 8.0 | ref:https://www.sciencedirect.com/topics/medicine-and-dentistry/alpha-wave |
   |node_strength_proportion | 0.5 | The amount that the node strengths affect the intrinsic frequencies of each region i.e. hubs will have higher node strengths and therfore a stronger "pull" (intrinsic frequency) |
   |physical_distance_proportion | 1 - (node_strength_proportion) | The rest of the intrinsic frequency is determined by physical distance between regions|

   </details>

   <details>
   <summary>Coupling Constant SweepCoupling Constant Sweep Parameters</summary>
    
   | Parameter | Value | Justification |
   | :--- | :--- | :--- |
   |sigma | (alpha_max - alpha_min)*2*np.pi / np.sqrt(alpha_max) | std for alpha frequency range|
   |k_max_factor | 10.0 | |
   |number_of_k_values | 25 | |
   
   </details>
