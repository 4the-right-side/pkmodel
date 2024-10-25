#
# Protocol class
#
from pkmodel import Model
import numpy as np

class Protocol(Model):
    """A Pharmokinetic (PK) protocol
    """
    def __init__(self,args_dict, start_h = 0, stop_h = 240, duration_h = 2, freq_h = 24):
        super().__init__(args_dict)
        self.add_dose_t_tophat_params(start_h, stop_h, duration_h, freq_h)

    def dose(self, t):
        """
        The Dose function that drives the system. 

        Parameters
        ----------
        start_h: the initial time where the model begins solving

        stop_h : the final time where the model stops solving 

        duration_h : the length of time of the dose pulse.

        freq_h: the frequency at which the pulse repeats 

        Note the height of the top hat function is given by 'X' in models.py

        Outputs
        -------
        A value either 0 or X at each t

        """
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
        r"""
        The RHS of the bolus ODE system which solves the following system:

        .. math::

            \frac{dq_c}{dt} &= \text{Dose}(t) - \frac{q_c}{V_c} CL 
            - Q_{p1} \left(\frac{q_c}{V_c} - \frac{q_{p1}}{V_{p1}}\right) \\
            \frac{dq_{p1}}{dt} &= Q_{p1} \left(\frac{q_c}{V_c} - \frac{q_{p1}}{V_{p1}}\right)

        Parameters
        ----------
        Q_p1, V_c, V_p1, CL, k_a, N
        Note that k_a and q_0 are not used for the Bolus model. dq_0/dt = 0 for all t.

        """
        q_0 ,q_c, q_p1 = y
        dq_0_dt = 0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = self.dose(t) - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [ dq_0_dt, dqc_dt, dqp1_dt]

    def subcut_rhs(self, t, y, Q_p1, V_c, V_p1, CL, k_a, N):
        r"""
        The RHS of the bolus ODE system which solves the following system:

        .. math::

            \frac{dq_0}{dt} &= \text{Dose}(t) - k_{a} q_{0} \\
            \frac{dq_c}{dt} &=  k_{a} q_{0} - \frac{q_c}{V_c} CL - Q_{p1} \left(\frac{q_c}{V_c} - \frac{q_{p1}}{V_{p1}}\right) \\
            \frac{dq_{p1}}{dt} &= Q_{p1} \left(\frac{q_c}{V_c} - \frac{q_{p1}}{V_{p1}}\right)

        Parameters
        ----------
        Q_p1, V_c, V_p1, CL, k_a, N
        """
        q_0 , q_c, q_p1 = y
        dq0_dt = self.dose(t) - k_a * q_0
        transition = N * Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = k_a * q_0  - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [dq0_dt , dqc_dt, dqp1_dt]   

if __name__ == "__main__":
    import models 
    model = Protocol( args_dict = models.model1)
    print(model.dose(0))
    print(model.dose(25))
    print(model.dose(24))
