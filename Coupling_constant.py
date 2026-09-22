import numpy as np 
from kuramoto import generting_intrinstic_frequencies, run_kuramoto

connectome = np.load('origional_connectome.npy') # Initial starting matrix - same for every run
size = np.size(connectome, axis=0) # n.o. nodes
np.random.seed(10)

def K_c():
    """
    Returns theoreical critical threshold value of K.
    """
    intrinsic_frequencies = generting_intrinstic_frequencies()
    K_crit = np.sqrt(2 / np.pi) * np.sqrt(5.24) # Looked up formula
    return K_crit


def running_kuromoto():
    """
    Sweeps over ranger of K values and runs the kuromoto.py for the origional connectome.
    Saves each of the final outcomes.
    """
    K_crit = K_c()
    K_values = np.arange(0, 3 * K_crit, 0.5) # Set steps as 3 values for now
    # Also K_crit is not uppder limit bc its theoretical? so x3 

    for K in K_values:
        Weights_record = run_kuramoto(K)
        #np.save('pruned_weights.npy', np.array(Weights_record, dtype=object), allow_pickle=True) 
        # Saving the whole thing for each might be too much???
        Final_outcome = Weights_record[-1]
        np.save(f'{K}_final_pruned_weight.npy', Final_outcome) 

running_kuromoto()     
# NOTES
# Just see if it runs for a few steps in K 
# Maybe plot the finals to see
# Figure out how to calc and use kuromoto order param to eval (r(t))
