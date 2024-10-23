#
# Protocol class
#

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
    
    def dose(self , t , X):
        #lets start with one top hat...
        self.add_dose #not finished here
        if t < start_h:
            return 0
        elif start_h < t < stop_h:
             return 
        elif t > stop_h:
            return 0

        
    def bolus_rhs(self, t, y, Q_p1, V_c, V_p1, CL, X):
            q_c, q_p1 = y
            transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
            dqc_dt = self.dose(t, X) - q_c / V_c * CL - transition
            dqp1_dt = transition
            return [dqc_dt, dqp1_dt]

    def subcut_rhs(self, t, y, Q_p1, V_c, V_p1, CL, X):
            q_c, q_p1 = y
            transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
            dqc_dt = self.dose(t, X) - q_c / V_c * CL - transition
            dqp1_dt = transition
            return [dqc_dt, dqp1_dt]   

if __name__ == "__main__":
      import models
      model = Protocol(name = "model1", args_dict = models.model1) #, dose_t_tophat_params=[1,1,1,1]) 