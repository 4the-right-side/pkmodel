#
# Protocol class
#
from model import Model
import numpy as np

class Protocol(Model):
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------
    need to have attributes for the possible functions and does function?
    value: numeric, optional
        an example paramter

    """
    def __init__(self, name, args_dict, start_h = 0, stop_h = 240, duration_h = 2, freq_h = 24):
        super().__init__(name, args_dict)
        self.add_dose_t_tophat_params(start_h, stop_h, duration_h, freq_h)

    def dose(self, t):
        #lets start with one top hat...
        start_h = self.dose_t_tophat_params[0]
        stop_h = self.dose_t_tophat_params[1]
        duration_h = self.dose_t_tophat_params[2]
        freq_h = self.dose_t_tophat_params[3]
        
        if t < start_h:
            return 0
        elif t > stop_h:
            return 0
        else:
            ind = np.floor(t / freq_h)
            hours_after_dosing = (t / freq_h) - ind
            duration_frac = duration_h / freq_h
            if hours_after_dosing < duration_frac:
                return self.dose_t_tophat_params[-1] # returning X
            else:
                return 0

        
    def bolus_rhs(self, t, y, Q_p1, V_c, V_p1, CL, k_a, N):
        q_c, q_p1, q_0 = y
        dq_0_dt = 0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = self.dose(t) - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [ dqc_dt, dqp1_dt, dq_0_dt]

    def subcut_rhs(self, t, y, Q_p1, V_c, V_p1, CL, k_a, N):
        q_0 , q_c, q_p1 = y
        dq0_dt = self.dose(t) - k_a * q_0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = k_a * q_0  - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [dq0_dt , dqc_dt, dqp1_dt]   

if __name__ == "__main__":
    import models 
    model = Protocol(name = "model1", args_dict = models.model1)
    print(model.dose(0))
    print(model.dose(25))
    print(model.dose(24))
