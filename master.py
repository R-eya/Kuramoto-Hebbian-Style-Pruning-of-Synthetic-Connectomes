import numpy as np
from generating_connectomes import generating_connectomes
from Coupling_constant import K_values
from kuramoto import Kuromoto_K_Sweep
from plot import plotting_loop



def main():
    time_steps = 400 
    synthetic_origional = generating_connectomes()
    K_values_list, K_crit = K_values(W=synthetic_origional)
    Results = Kuromoto_K_Sweep(W=synthetic_origional, K_values_list=K_values_list, time_steps=time_steps)
    plotting_loop(Results=Results, synthetic_origional=synthetic_origional, K_values_list=K_values_list)

main()


#### Figure out what timeframe to use and calc timesteps accordingly -- a lot of papers take 1000 weight updates as 1 year
# Look into that cuz the network changes a lot for just 500
# Figure out why is looks like connections are being created 
#### Run the real vs null check (but fix it bc z score may not be best to check)
#### Understant the kuromoto param r(t) and use the run analysis