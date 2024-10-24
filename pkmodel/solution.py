#
# Solution class
#
import scipy.integrate
import numpy as np
import matplotlib.pylab as plt
from model import Model
from protocol import Protocol


class Solution(Model):
    """A Pharmokinetic (PK) solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, args_dict , t_eval, y0):
        super().__init__(args_dict)
        self.t_eval = t_eval
        self.y0 = y0


    def solve(self):
        """
        A function that solves the ODE system for the model imported

        inputs: A list of models from models.py, a numpy array of the times to solve
        and a y0 for initial values.
        """
        current_protocol = Protocol(args_dict = self.args_dict)
        param_vals = list(self.args_dict.values())
        Q_p1 , V_c , V_p1 , CL , ka = param_vals[1:6]
        N = self.number_of_peripheral_compartments
        print(t_eval)
        print(N)
        if model['Dosing_Type'] == 'Sub':
            print('subcutaneous model')
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_protocol.subcut_rhs(t, y, Q_p1 , V_c , V_p1 , CL , ka , N),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval)
        elif model['Dosing_Type'] == 'Bolus':
            print('Bolus model')
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_protocol.bolus_rhs(t, y, Q_p1 , V_c , V_p1 , CL , ka , N),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval)
        np.savez(model['name'] , t= self.solution.t ,
                     q0 = self.solution.y[0], qc= self.solution.y[1],  q1= self.solution.y[2])
    


    def Plot(self):
        solution = np.load(model['name'] + '.npz')
        t= solution['t']
        q0 = solution['q0']
        qc = solution['qc']
        q1 = solution['q1']
        fig, ax = plt.subplots()
        ax.plot(t , qc)
        ax.plot(t , q1)
        ax.figure.savefig('Plot for model' + model['name'])
        plt.show()


        
                      
if __name__ == "__main__":
      import models
      t_eval = np.linspace( 0 ,1 ,1000)
      y0 = np.array([0.0, 0, 0])
      model = models.model1
      sol = Solution(args_dict = model, t_eval= t_eval , y0 = y0)
      sol.define_peripheral_compartments(1)
      sol.solve() 
      sol.Plot()
