import numpy as np
from generating_connectomes import generating_connectomes
from Coupling_constant import K_values
from kuramoto import Kuromoto_K_Sweep
from plot import plotting_loop



def main():
    synthetic_origional = generating_connectomes()
    K_values_list, K_crit = K_values(W=synthetic_origional)
    Results = Kuromoto_K_Sweep(W=synthetic_origional, K_values_list=K_values_list)
    plotting_loop(Results=Results, synthetic_origional=synthetic_origional, K_values_list=K_values_list)


