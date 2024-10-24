#
# Solution class
#
import scipy.integrate
import numpy as np
import matplotlib.pylab as plt
from model import Model
from protocol import Protocol


class Solution:
    """A Pharmokinetic (PK) solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, models_to_run , t_eval, y0):
        self.t_eval = t_eval
        self.y0 = y0
        self.models_to_run = models_to_run


    def solve(self):
        """
        A function that solves the ODE system for the list of models inputed

        inputs: A list of models from models.py, a numpy array of the times to solve
        and a y0 for initial values.
        """
        fig_central, ax_central = plt.subplots()
        fig_peripheral, ax_peripheral= plt.subplots()
        ax_central.set_title('Central compartment')
        ax_peripheral.set_title('Peripheral compartment')

        for model in self.models_to_run:
            print('solving model')
            current_protocol = Protocol(name = model['name'], args_dict = model)
            current_protocol.define_peripheral_compartments(1)
            if model['Dosing_Type'] == 'Sub':
                print('subcutaneous model')
                self.solution = scipy.integrate.solve_ivp(
                fun=lambda t, y: current_protocol.subcut_rhs(t, y, current_protocol.args_dict['Q_p1'], 
                                    current_protocol.args_dict['V_c'], current_protocol.args_dict['V_p1'], 
                                    current_protocol.args_dict['CL'],
                                    current_protocol.args_dict['ka'],
                                    current_protocol.number_of_peripheral_compartments),
                t_span=[self.t_eval[0], self.t_eval[-1]],
                y0=self.y0, t_eval=self.t_eval)
            elif model['Dosing_Type'] == 'Bolus':
                print('Bolus model')
                self.solution = scipy.integrate.solve_ivp(
                fun=lambda t, y: current_protocol.bolus_rhs(t, y, current_protocol.args_dict['Q_p1'], 
                                    current_protocol.args_dict['V_c'], current_protocol.args_dict['V_p1'], 
                                    current_protocol.args_dict['CL'],
                                    current_protocol.args_dict['ka'],
                                    current_protocol.number_of_peripheral_compartments),
                t_span=[self.t_eval[0], self.t_eval[-1]],
                y0=self.y0, t_eval=self.t_eval)
            ax_central.plot(self.solution.t , self.solution.y[1], label = current_protocol.name)
            ax_peripheral.plot(self.solution.t , self.solution.y[2], label = current_protocol.name)
        ax_central.legend()
        ax_peripheral.legend()
        plt.show()
              
if __name__ == "__main__":
      import models
      t_eval = np.linspace( 0 ,1 ,1000)
      y0 = np.array([0.0, 0.0, 0.0])
      models_to_run = [models.model1, models.model2]
      sol = Solution(models_to_run= models_to_run, t_eval= t_eval , y0 = y0)
      sol.solve() 
      #sol.Plot()
