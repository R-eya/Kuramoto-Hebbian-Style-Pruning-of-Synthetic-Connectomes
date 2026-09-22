import numpy as np 
connectome = np.load('origional_connectome.npy') # Initial starting matrix - same for every run
size = np.size(connectome, axis=0) # n.o. nodes
np.random.seed(10)


def weights_to_phase():
    """
    Calculates the initial phases from the 
    weights by using the first node as stationary frame.
    """
    W_i1 = connectome[0] # Takes first row as initial i.e. make the first node the stationary frame 
    # so all phases are teken relative to that node
    prop_const = 2 * np.pi / np.max(W_i1) # map so that it spans 0 to 2pi
    initial_phases = prop_const * W_i1
    initial_phase_diff_mat = phase_diff(initial_phases)
    return initial_phases, initial_phase_diff_mat

def phase_diff(phases):
    """
    Returns a pairwise phase difference matrix between each pair of nodes.
    """
    return phases[:, None] - phases[None, :] # Nx1 minus 1xN (i.e. j flips ones of the and subtracts pairwise)

def generting_intrinstic_frequencies():
    """
    Guassian dist for assigning intrinsic frequesncies.
    Uses average alpha frequency.
    """
    intrinsic_freq = np.random.normal(loc = 65.97, scale= 5.24, size=size) # Narrow Guassian with mean alpha freq
    return intrinsic_freq


def Kuramoto(phase, intrinsic_freq, phase_diff_mat):
    """
    Runs one timestep on Kuromoto Model.
    Returns new phases (1xN) and the pairwise new phase difference matrix (NxN).
    """
    phase_diff_mat_avg = phase_diff_mat / np.mean(phase_diff_mat)
    K = 1
    dtheta_dt = intrinsic_freq + K*np.sum(np.sin(phase_diff_mat_avg), axis = 1)
    dt = 0.01
    next_phase = phase + dtheta_dt*dt
    phase_diff_next = phase_diff(next_phase)
    return next_phase, phase_diff_next

def weight_update(W, phase_diff_t, phase_diff_next):
    """
    Thresholds.
    Uses the change is the phase difference between time steps to prune matrix.
    """
    beta = np.zeros_like(W)
    mask = W > 0.05 # thresholding
    beta[mask] = (100 * W[mask])**-1 # Ensures big weights dont massivelt dominate at start
    delta_phase = np.abs(phase_diff_t) - np.abs(phase_diff_next) # Are nodes getting more or less in sync?
    return W + beta*np.sin(delta_phase)


def run_kuramoto():
    """
    Main loop.
    """
    Weights_record = [connectome] # Record of all the weight matrices
    W = connectome

    initial_phases, initial_phase_diff_mat = weights_to_phase()
    intrinsic_freq = generting_intrinstic_frequencies()
    phases, phase_diff_mat = initial_phases, initial_phase_diff_mat

    for t in range(1000):

        next_phase, phase_diff_next = Kuramoto(phase=phases, intrinsic_freq=intrinsic_freq, phase_diff_mat=phase_diff_mat)
        W_new = weight_update(W, phase_diff_mat, phase_diff_next)

        if t % 100 == 0:
            Weights_record.append(W_new) # Only add every 100 timesteps to save mem
        W = W_new
        phases = next_phase
        phase_diff_mat = phase_diff_next

    return Weights_record

Weights_record = run_kuramoto()
np.save('pruned_weights.npy', np.array(Weights_record, dtype=object), allow_pickle=True)





    
