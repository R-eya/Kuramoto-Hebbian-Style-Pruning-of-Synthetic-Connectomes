import numpy as np 


def generting_intrinstic_frequencies(size, rng=None):
    rng = np.random.default_rng() if rng is None else rng
    return rng.normal(loc=65.97, scale=5.24, size=size)

def phase_diff(phases):
    """
    Returns a pairwise phase difference matrix between each pair of nodes.
    """
    return phases[:, None] - phases[None, :] # Nx1 minus 1xN (i.e. j flips ones of the and subtracts pairwise)

def Kuramoto(phase, intrinsic_freq, phase_diff_mat, W, K=1):
    """
    Runs one timestep on Kuromoto Model.
    Returns new phases (1xN) and the pairwise new phase difference matrix (NxN).
    """
    dtheta_dt = intrinsic_freq - K*np.sum(W * np.sin(phase_diff_mat), axis = 1)
    dt = 0.01
    next_phase = phase + dtheta_dt*dt
    phase_diff_next = phase_diff(next_phase)
    return next_phase, phase_diff_next

def weight_update(W, phase_diff_t, phase_diff_next, eta=5e-4, w_min=0.05):
    """
    Hebbian thresholding.
    Uses the change is the phase difference between time steps to prune matrix.
    """
    sync = np.cos(phase_diff_next)    # >0 if the pair became more in phase
    W_new = W.copy()
    edges = W > 0
    W_new[edges] += eta * sync[edges]
    W_new = np.clip(W_new, 0, 1)
    W_new[W_new < w_min] = 0                      # actual pruning; zeros never revive
    return W_new

def wrap(delta):
    return np.angle(np.exp(1j * delta))

def run_kuramoto(K, connectome, seed = 10):
    """
    Main Kuromoto loop.
    """
    #connectome = np.load('origional_connectome.npy') # Initial starting matrix - same for every run
    W = connectome
    size = np.size(W, axis=0) # n.o. nodes 
    


    Weights_record = [W] # Record of all the weight matrices

    rng = np.random.default_rng(seed)

    phases = rng.uniform(0, 2 * np.pi, size)          # random start
    intrinsic_freqs = generting_intrinstic_frequencies(size, rng)
    intrinsic_freqs = intrinsic_freqs - intrinsic_freqs.mean()
    phase_diff_mat = phase_diff(phases)

    for t in range(1000):

        next_phase, phase_diff_next = Kuramoto(phase=phases, intrinsic_freq=intrinsic_freqs, phase_diff_mat=phase_diff_mat, W=W, K=K)
        W_new = weight_update(W, phase_diff_mat, phase_diff_next)

        if t % 100 == 0:
            Weights_record.append(W_new) # Only add every 100 timesteps to save mem
        W = W_new
        phases = next_phase
        phase_diff_mat = phase_diff_next
    Weights_record.append(W_new)
    return Weights_record

def Kuromoto_K_Sweep(W, K_values_list):
    """
    Sweeps over ranger of K values and runs kuromoto.
    Saves each of the final outcomes.
    """

    Results = []

    for K in K_values_list:
        Weights_record = run_kuramoto(K, connectome=W)
        Final_outcome = Weights_record[-1]
        Results.append(Final_outcome)
    return Results

