#
# Model class
#
import scipy.integrate
import matplotlib.pylab as plt
import numpy as np


#The idea is there will be an args_dict with all the parameters, including the name of the function?

def dose(t, X):
    return X

def rhs(t, y, Q_p1, V_c, V_p1, CL, X):
    q_c, q_p1 = y
    transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
    dqc_dt = dose(t, X) - q_c / V_c * CL - transition
    dqp1_dt = transition
    return [dqc_dt, dqp1_dt]


args_dict = {
    'name': 'model1',
    'Q_p1': 1.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 1.0,
    'X': 1.0,
}

class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, name , args_dict):
        self.name = name
        self.args_dict = args_dict


    def solve(self, t_eval, y0):
        """
        Solve the ODE using ivp model
        :param t_eval: time points as input to the solver.
        """

        self.solution = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs(t, y, self.args_dict['Q_p1'], 
                             self.args_dict['V_c'], self.args_dict['V_p1'], 
                             self.args_dict['CL'],
                             self.args_dict['X']),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval)
    
    def plot(self):
        plt.plot(self.solution.t , self.solution.y[0])
        plt.show()


t_eval = np.linspace(0 , 1 , 100)
y0 = np.array([0.0, 0.0])
PK_model = Model(name = 'model1' , args_dict = args_dict)
PK_model.solve(t_eval, y0)
PK_model.plot()







