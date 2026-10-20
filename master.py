from config import Config
from generating_connectomes import Connectome_Generator
from Coupling_constant import K_values
from kuramoto import K_Sweep
from plot import ConnectomePlotter

def main(cfg :Config = Config()):
    generator = Connectome_Generator(cfg)
    W_0 = generator.generate_connectome()

    K_vals, K_c = K_values(W_0, cfg)

    results = K_Sweep(W_0, K_values=K_vals, cfg=cfg)

    plotter = ConnectomePlotter()
    plotter. plot_sweep(W0=W_0, Results=results, K_values=K_vals, save_path="Comparison_Kvals.png",row_indices=None)

    return W_0, K_vals, K_c, results


if __name__ == "__main__":
    main()

#### Figure out what timeframe to use and calc timesteps accordingly -- a lot of papers take 1000 weight updates as 1 year
# Look into that cuz the network changes a lot for just 500
# Figure out why is looks like connections are being created 
#### Run the real vs null check (but fix it bc z score may not be best to check)
#### Understant the kuromoto param r(t) and use the run analysis