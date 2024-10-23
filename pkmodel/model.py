#
# Model class
#
import scipy.integrate
import matplotlib.pylab as plt
import numpy as np
import importlib
import models
importlib.reload(models)
from solution import Solution
#importlib.reload(solution)


#The idea is there will be an args_dict with all the parameters, including the name of the function?

def dose(t, X):
    return X



args_dict = models.model1

"""
{
    'name': 'model1',
    'Q_p1': 1.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 1.0,
    'X': 1.0,
    'Sub' : False,
    'Bolus' : True
}

"""

class Model_ed:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, name , args_dict):
        self.name = name
        self.args_dict = args_dict


    def bolus_rhs(self, t, y, Q_p1, V_c, V_p1, CL, X):
            q_c, q_p1 = y
            transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
            dqc_dt = dose(t, X) - q_c / V_c * CL - transition
            dqp1_dt = transition
            return [dqc_dt, dqp1_dt]

    def subcut_rhs(self, t, y, Q_p1, V_c, V_p1, CL, X):
            q_c, q_p1 = y
            transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
            dqc_dt = dose(t, X) - q_c / V_c * CL - transition
            dqp1_dt = transition
            return [dqc_dt, dqp1_dt]   
    """
    def solve(self, t_eval, y0):
        if args_dict['Sub']:

            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.subcut_rhs(t, y, self.args_dict['Q_p1'], 
                                self.args_dict['V_c'], self.args_dict['V_p1'], 
                                self.args_dict['CL'],
                                self.args_dict['X']),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0, t_eval=t_eval)

        elif args_dict['Bolus']:

            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.bolus_rhs(t, y, self.args_dict['Q_p1'], 
                                self.args_dict['V_c'], self.args_dict['V_p1'], 
                                self.args_dict['CL'],
                                self.args_dict['X']),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0, t_eval=t_eval)
        
    def plot(self):
        plt.plot(self.solution.t , self.solution.y[0])
        plt.show()
    """

    


    

    


t_eval = np.linspace(0 , 1 , 100)
y0 = np.array([0.0, 0.0])
models_to_run = ['model1', 'model1']


## For small testing; to be deleted later
if __name__ == "__main__":
    import models
    import solution
    sol = Solution(models_to_run=models_to_run , t_eval=t_eval , y0 = y0)
    sol.solve()
    sol.plot()








