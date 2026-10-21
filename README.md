# CC Pruning 
Description


## Flow Chart 

```mermaid
flowchart LR

    subgraph Inputs ["Data sources"]
        direction TB
        Q[("Schaefer 2018 atlas<br/>(100 ROIs)")]
        A[("Nilearn developmental fMRI")]
    end
    style Inputs fill:#e8f4fd,stroke:#2b6cb0,stroke-width:2px

    Q[("Schaefer 2018 Atlas <br> (100 ROIs)")] -->|Extract Euclidian Distances| W[Connection Probability Model] -->C

    G([Calculate Intrinsic Frequencies for each node]) --> E[Kuramoto Dynamics]
    A[(Nilearn Developmental fMRI)] -->B[Reference fMRI Metrics]--> C(("Compare Graph Metrics <br> (Minimise RMSD)" )) -->|Sweep over d_0 | D[Create Calibrated Synthetic Connectome]
    D --> E

    F([Calculate Critical Coupling Constant]) --> E

    subgraph Sweep ["Coupling constant sweep"]
        direction TB
        E["Kuramoto dynamics"]
        H["Hebbian pruning"]
        E <-->|"Update Weights"| H
    end
style Inputs fill:#fde8ef,stroke:#fde8ef,stroke-width:2px
style Sweep fill:#e6fffa,stroke:#e6fffa,stroke-width:2px
```

## Model Decisions
### Connectome Generation
$$
P_{ij} = A \exp\left(-\frac{D_{ij}}{d_0}\right)
$$

- $D_{ij}$: Euclidean distance between regions $i$ and $j$
- $d_0$: spatial scale of the distance cost, fitted by sweeping over a range of values
- $A$: fixed scaling factor (`scaling_factor = 10` in `config.py`)

### Kuramoto Equation
# NOTE USE THE IPYNB TO ADD TO README ALSO LOOK THROUGH PAPER NOTEBOOK


### Coupling Constant
 $K_c = \sigma \sqrt{8 / \pi} / \lambda_{max}$
 






## Configuration Decisions
 
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
