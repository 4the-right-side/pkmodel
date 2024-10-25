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
    Inherits model paramters from the Model class

    """
    def __init__(self, args_dict , t_eval, y0):
        super().__init__(args_dict)
        self.t_eval = t_eval
        self.y0 = y0
    

    def solve(self, start_h = 0, stop_h = 240, duration_h = 24, freq_h = 24):
        """
        A function that solves the ODE system for the model imported

        Parameters
        ----------
        A list of models from models.py, a numpy array of the times to solve (t_eval)
        and a y_0 array for initial values.

        outputs
        -------
        saves a file with t, q_0 , q_c and q_1 saved as numpy arrays. saves as "modelname".npz.
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

        y_dose = np.zeros(self.t_eval.shape)
        for i in range(len(self.t_eval)):
            y_dose[i] = current_protocol.dose(self.t_eval[i])
        np.savez(self.args_dict['name'] , t= self.solution.t ,
                     q0 = self.solution.y[0], qc= self.solution.y[1],  qp1= self.solution.y[2], y_dose = y_dose)
    


    def Plot(self):
        """A function that plots the saved numpy arrays.
        
        Parameters
        ----------
        None, uses a saved numpy file from Solution.solve()
        
        Outputs
        -------
        Will plot q_c and q_1 on the same graph and save to a .png file
    
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

        fig_dose , ax_dose = plt.subplots()
        y_dose = solution['y_dose']
        ax_dose.set_title('Dose Function', fontsize = 18)
        ax_dose.set_xlabel('time',  fontsize = 18)
        ax_dose.set_ylabel('Drug Quantity (ng)',  fontsize = 18)
        ax_dose.plot(self.t_eval , y_dose)
        ax_dose.figure.savefig('dose_function' + '.png')

                 
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
