#
# Solution class
#
import scipy.integrate
import numpy as np
import matplotlib.pylab as plt
from pkmodel import Model
from pkmodel import Protocol


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


    def solve(self, start_h = 0, stop_h = 240, duration_h = 24, freq_h = 24):
        """
        A function that solves the ODE system for the model imported

        inputs: A list of models from models.py, a numpy array of the times to solve
        and a y0 for initial values.

        ouputs: saves a file with t, q0 , qc and q1 saved as numpy arrays
        """
        current_protocol = Protocol(args_dict = self.args_dict, start_h = start_h, stop_h = stop_h, duration_h = duration_h, freq_h = freq_h)
        param_vals = list(self.args_dict.values())
        Q_p1 , V_c , V_p1 , CL , ka = param_vals[1:6]
        N = self.number_of_peripheral_compartments
        if self.args_dict['Dosing_Type'] == 'Sub':
            print('subcutaneous model')
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_protocol.subcut_rhs(t, y, Q_p1 , V_c , V_p1 , CL , ka , N),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval)
        elif self.args_dict['Dosing_Type'] == 'Bolus':
            print('Bolus model')
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_protocol.bolus_rhs(t, y, Q_p1 , V_c , V_p1 , CL , ka , N),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval)
        np.savez(self.args_dict['name'] , t= self.solution.t ,
                     q0 = self.solution.y[0], qc= self.solution.y[1],  qp1= self.solution.y[2])
    


    def Plot(self):
        """
        A function that plots the saved numpy arrays. 
        
        inputs: None, uses a saved numpy file from Solution.solve()
        
        Outputs: Will plot qc and q1 on the same graph
    
        """
        solution = np.load(self.args_dict['name'] + '.npz')
        t= solution['t']
        q0 = solution['q0']
        qc = solution['qc']
        q1 = solution['qp1']
        fig, ax = plt.subplots()
        ax.plot(t , qc, label = r'$q_c$')
        ax.plot(t , q1, label = r'$q_{p1}$')
        ax.legend(fontsize = 15)
        ax.set_title('Solution for ' + self.args_dict['name'], fontsize = 18)
        ax.set_xlabel('time',  fontsize = 18)
        ax.set_ylabel('Drug Quantity (ng)',  fontsize = 18)
        ax.figure.savefig(self.args_dict['name'] + '.png')

                 
if __name__ == "__main__":

      import models
      t_eval = np.linspace( 0 ,10 ,10000)
      y0 = np.array([0.0, 0, 0])
      models_to_run = [models.model1]
      model = models.model1
      sol = Solution(args_dict = model, t_eval= t_eval , y0 = y0)
      sol.define_peripheral_compartments(1)
      sol.solve() 
      sol.Plot()
