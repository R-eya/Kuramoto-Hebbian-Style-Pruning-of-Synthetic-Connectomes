# 🧠 Kuramoto-Hebbian Style Pruning of Synthetic Connectomes

## 📝 Overview
Simulating early neurodevelopmental pruning with Kuramoto Oscillators and Hebbian Plasticity. <br>
**Motivation:** fMRI data for children in early developmental stages is limited. The first stage aims to calibrate a synthetic connectome, (using a probability of connection model that decays exponentially with distance between regions) and forces a fixed high density of the top 70% of connections to imitate highly dense infant connectomes. <br>
Followed by Kuramoto-Hebbian style pruning. <br>
**The Project Asks:** <br>
❓Can a simplified Kuramoto model, alongside Hebbian-like pruning, reproduce early biological neurodevelopment in a synthetically generated connectome?
❓How does the Kuramoto Coupling Strength affect the graph metrics of the resulting connectomes?
❓Can the resulting connectomes be classified into Autistic (ASD), Neurotypical (NT) and Schizophrenic (SZ) characteristic connectomes.

It is intended to explore how a single control parameter (coupling strength K) changes network organisation, which may inform how future, more realistic models are designed.

## Flow Chart 

```mermaid
flowchart LR

    subgraph Inputs ["Data sources"]
        direction TB
        Q[("Schaefer 2018 atlas<br/>(100 ROIs)")]
        A[("Nilearn developmental fMRI")]
    end

    Q[("Schaefer 2018 Atlas <br> (100 ROIs)")] -->|Extract Euclidean Distances between ROIs| W[Connection Probability Model] -->C

    A[(Nilearn Developmental fMRI)] -->B[Reference fMRI Metrics]--> C(("Compare Graph Metrics <br> (Minimise RMSD)" )) -->|Sweep over d_0 | D[Create Calibrated Synthetic Connectome]
    
    %% Route D to E through an invisible node inside the subgraph
    D --> HiddenNode --> E[Kuramoto Dynamics]

    subgraph kurma ["Kuramoto Parameters"]
        direction TB
        HiddenNode[" "]:::hidden
        G([Calculate Intrinsic Frequencies for each node])
        F([Calculate Critical Coupling Constant])
    end

    subgraph Sweep ["Coupling constant sweep"]
        direction TB
        E["Kuramoto dynamics"]
        H["Hebbian pruning"]
        E <-->|"Update Weights"| H
    end
        
    G --> E
    F --> E

style Inputs fill:#fde8ef,stroke:#fde8ef,stroke-width:2px
style Sweep fill:#e6fffa,stroke:#e6fffa,stroke-width:2px
style kurma fill:#fdf0e6,stroke:#fdf0e6,stroke-width:2px

%% Hide the passthrough node so the line looks continuous
classDef hidden display:none;
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
  
 | Parameter | Value | Justification | Source |
 | :--- | :--- | :--- | :--- |
 | n_rois | 100 | Memory | Schaefer et al. 2018 |
 | seed | 10 | Reproducibility | none |
 |scaling_factor | 10.0 | Representative of many strong connections in the early connectome. |  |    
 |noise_loc, noise_scale | 0.05, 0.05 | Small noise to replicate biological noise |  |
 | d0_range | 0-19 | Typical Value is 5-15 |  |
 |threshold_percent | 30 | Keeps top 70% of edges, dense to represent unpruned network | |

 </details>

  <details>
  <summary>Kuramoto Parameters</summary>
    
  | Parameter | Value | Justification | Source |
  | :--- | :--- | :--- | :--- |
  |dt | 0.01 | Integration Step| Convergence test |
  |eta| 5e-4 | Learning Rate | |
  |time_steps| 2000 | Running for 2 years | 1000 time-steps is approx 1 year between ages 1-2years |
  |w_min| 0.1| Pruning threshold | |
  |record_each| 100 | Storage - to be used to show the dynamic pruning| |
  |sync_reward, desync penalty| 0.5 | phase synchronisation is rewarded half as much as desynchronisation is penalised to mitigate random hubs forming due to noise|
  | intrinsic_frequency_effect | 5 | Modelling choice to promote hubs formings | |

  </details>

   <details>
   <summary>Intrinsic Frequency Parameters</summary>
  
   | Parameter | Value | Justification | Source |
   | :--- | :--- | :--- | :--- |
   |alpha_max, alpha_min| 12.0, 8.0| Alpha range band|  ref:https://www.sciencedirect.com/topics/medicine-and-dentistry/alpha-wave |
   |node_strength_proportion | 0.5 | The amount that the node strengths affect the intrinsic frequencies of each region i.e. hubs will have higher node strengths and therefore a stronger "pull" (intrinsic frequency) | Modelling choice|

   </details>

   <details>
   <summary>Coupling Constant Parameters</summary>
    
   | Parameter | Value | Justification | Source |
   | :--- | :--- | :--- | :--- |
   |sigma | (alpha_max - alpha_min)*2*np.pi / np.sqrt(12) | std for alpha frequency range| |
   |k_max_factor | 3.0 | Sweep of k goes up to k_max_factor*K_c| |
   |number_of_k_values | 25 | Resolution of K sweep| |
   
   </details>
