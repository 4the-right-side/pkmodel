#
# Protocol class
#
from model_pao import Model

class Protocol(Model):
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------
    need to have attributes for the possible functions and does function?
    value: numeric, optional
        an example paramter

    """
    def __init__(self, name, args_dict):
        super().__init__(name, args_dict)
    
    def dose(self, t):
        #lets start with one top hat...
        start_h, stop_h, duration_h, freq_h = 0, 240, 24, 24
        self.add_dose_t_tophat_params(start_h, stop_h, duration_h, freq_h) #Default is 10 days and administer the drug every 24 hours and the drug stays in the bosy for 24 hours.
        print(t)
        if t <= start_h:
            return 0
        elif start_h < t < stop_h:
            return self.dose_t_tophat_params[-1] 
        elif t > stop_h:
            return 0

        
    def bolus_rhs(self, t, y, Q_p1, V_c, V_p1, CL, k_a, N = 1):
        q_c, q_p1, q_0 = y
        dq_0_dt = 0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = self.dose(t) - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [ dqc_dt, dqp1_dt, dq_0_dt]

    def subcut_rhs(self, t, y, Q_p1, V_c, V_p1, CL, k_a, N = 1):
        q_0 , q_c, q_p1 = y
        dq0_dt = self.dose(t) - k_a * q_0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = k_a * q_0  - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [dq0_dt , dqc_dt, dqp1_dt]   

if __name__ == "__main__":
    import models 
    model = Protocol(name = "model1", args_dict = models.model1) 
    print(model.dose(20))
