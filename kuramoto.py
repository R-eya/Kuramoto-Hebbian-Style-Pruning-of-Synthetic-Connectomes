import numpy as np 
connectome = np.load('origional_connectome.npy')
size = np.size(connectome, axis=0)
np.random.seed(10)


def weights_to_phase():
    W_i1 = connectome[0]
    prop_const = 2 * np.pi / np.max(W_i1)
    initial_phases = prop_const * W_i1
    initial_phase_diff_mat = phase_diff(initial_phases)
    return initial_phases, initial_phase_diff_mat

def phase_diff(phases):
    return phases[:, None] - phases[None, :]

def generting_intrinstic_frequencies():
    intrinsic_freq = np.random.normal(loc = 65.97, scale= 5.24, size=size) # Narrow Guassian with mean alpha freq
    return intrinsic_freq


def Kuramoto(phase, intrinsic_freq, phase_diff_mat):
    dtheta_dt = intrinsic_freq + (1 / size)*np.sum(np.sin(phase_diff_mat), axis = 1)
    dt = 0.01
    next_phase = phase + dtheta_dt*dt
    phase_diff_next = phase_diff(next_phase)
    return next_phase, phase_diff_next

def weight_update(W, phase_diff_t, phase_diff_next):
    beta = np.zeros_like(W)
    mask = W > 0.05 # thresholding
    beta[mask] = (100 * W[mask])**-1
    delta_phase = np.abs(phase_diff_t) - np.abs(phase_diff_next)
    return W + beta*np.sin(delta_phase)


def run_kuramoto():
    Weights_record = [connectome]
    W = connectome
    initial_phases, initial_phase_diff_mat = weights_to_phase()
    intrinsic_freq = generting_intrinstic_frequencies()
    phases, phase_diff_mat = initial_phases, initial_phase_diff_mat
    for t in range(1000):
        next_phase, phase_diff_next = Kuramoto(phase=phases, intrinsic_freq=intrinsic_freq, phase_diff_mat=phase_diff_mat)
        W_new = weight_update(W, phase_diff_mat, phase_diff_next)
        if t % 100 == 0:
            Weights_record.append(W_new) # Only add every 100 timesteps
        W = W_new
        phases = next_phase
        phase_diff_mat = phase_diff_next
    return Weights_record

Weights_record = run_kuramoto()
np.save('pruned_weights.npy', np.array(Weights_record, dtype=object), allow_pickle=True)





    
