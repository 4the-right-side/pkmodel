#
# Solution class
#
import scipy.integrate
import numpy as np


class Solution(Model):
    """A Pharmokinetic (PK) solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, name, args_dict, models_to_run , t_eval, y0):
        super().__init__(name, args_dict)
        self.t_eval = t_eval
        self.y0 = y0
        self.models_to_run = models_to_run


    def solve(self):
        for model in self.models_to_run:
            print('solving model')
            current_model = Model(name = model, args_dict= models.model1)
            current_model.add_dose_t_tophat_params(10,100,1, 1)
            current_protocol = Protocol(name = "model1", args_dict = models.model1) 
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_protocol.subcut_rhs(t, y, current_model.args_dict['Q_p1'], 
                                current_model.args_dict['V_c'], current_model.args_dict['V_p1'], 
                                current_model.args_dict['CL'],
                                current_model.args_dict['X']),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval)

    def Plot(self):
        plt.plot(self.solution.t , self.solution.y[0])
        plt.show()
              
if __name__ == "__main__":
      import models
      t_eval = np.linspace( 0 ,1 ,10)
      y0 = np.array([0.0, 0.0])
      models_to_run = models.model1
      sol = Solution(name = "model1", args_dict = models.model1 , models_to_run= models_to_run, t_eval= t_eval , y0 = y0)
      sol.solve() 
      sol.Plot()