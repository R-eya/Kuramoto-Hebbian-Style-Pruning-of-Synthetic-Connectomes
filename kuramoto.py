import numpy as np 
from config import Config

### Maybe make a kuromoto class? Yes do this

class Kuramoto:
    def __init__(self, W_0, K, generator, cfg: Config = Config()):
        self.cfg = cfg
        self.K = K
        self.generator = generator

        self.W = np.asarray(W_0, dtype=float).copy()
        self.bin = (self.W > 0).astype(int)
        self.size = self.W.shape[0]

        rng = np.random.default_rng(cfg.seed)
        self.phases = rng.uniform(-np.pi, np.pi, self.size)   
        omegas = self.intrinsic_frequencies(self, self.W)
        self.omegas = omegas - omegas.mean()                
        self.phase_diff_mat = self.phase_diff(self.phases)

        self.record = [self.W.copy()]

    def __getattr__(self, attr):
        return getattr(self.generator, attr)

    @staticmethod
    def intrinsic_frequencies(self, W):
        """
        Returns intrinstic angular frequencies.
        By scaling the node strength and the physical distance to the alpha frequency scale (8-12Hz)
        """
        node_strengths = np.sum(W, axis = 1)
        alpha_max, alpha_min = self.cfg.alpha_max , self.cfg.alpha_min
        alpha_range = alpha_max - alpha_min

        omegas_NS = alpha_min + alpha_range*(node_strengths -  node_strengths.min()) / (node_strengths.max() - node_strengths.min())
        x, y, z = self.roi_coordinates[:, 0], self.roi_coordinates[:, 1], self.roi_coordinates[:, 2]
        z_impact = alpha_min + alpha_range*(z -  z.min()) / (z.max() - z.min())
        complex_phases = np.angle(x + 1j* y)
        xy_impact = alpha_min + alpha_range*(complex_phases -  complex_phases.min()) / (complex_phases.max() - complex_phases.min())
        omega_DIST = 0.5*z_impact + 0.5*xy_impact
        frequencies =  self.cfg.node_strength_proportion*omegas_NS + self.cfg.physical_distance_proportion*omega_DIST
        return frequencies * 2*np.pi
    
    @staticmethod
    def phase_diff(phases):
        """
        Returns a pairwise phase difference matrix between each pair of nodes.
        """
        return phases[:, None] - phases[None, :] # Nx1 minus 1xN (i.e. j flips ones of the and subtracts pairwise)

    def Kuramoto_equation(self):
        """
        Runs one timestep on Kuromoto Model.
        Returns new phases (1xN) and the pairwise new phase difference matrix (NxN).
        """
        dtheta_dt = (self.cfg.intrinsic_frequency_effect)*self.omegas - self.K*np.sum(self.bin * self.W * np.sin(self.phase_diff_mat), axis = 1)
        next_phase = self.phases + dtheta_dt * self.cfg.dt
        return next_phase, self.phase_diff(next_phase)

    def weight_update(self, phase_diff_next):
        """
        Hebbian thresholding.
        Uses the change is the phase difference between time steps to prune matrix.
        """
        sync = np.cos(phase_diff_next) # ensure it is only pruning and not growing connections 
        W_new = self.W.copy()
        edges = self.W > 0
        scaler = np.where(sync > 0, self.cfg.sync_reward, self.cfg.desync_penalty)
        W_new[edges] += self.cfg.eta * sync[edges] * scaler[edges]
        W_new = np.clip(W_new, 0, 1)
        W_new[W_new < self.cfg.w_min] = 0                    
        return W_new

    def run(self):
        for t  in range(self.cfg.time_steps):
            next_phases, phase_diff_next = self.Kuramoto_equation()
            W_new = self.weight_update(phase_diff_next)

            if t % self.cfg.record_each == 0:
                self.record.append(W_new)

            self.W = W_new
            self.phases =  next_phases
            self.phase_diff_mat = phase_diff_next

        self.record.append(self.W)
        return self.record

    @property
    def final_weights(self):
        return self.record[-1]


def K_Sweep(W_0, K_values, generator, cfg: Config = Config()):
    return [Kuramoto(W_0=W_0, K=K, generator=generator, cfg=cfg).run()[-1] for K in K_values]