#
# Solution class
#

class Solution:
    """A Pharmokinetic (PK) solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, models_to_run, t_eval ,y0): #models to run is a list of model names?
        self.models_to_run = models_to_run
        self.t_eval = t_eval
        self.y0 = y0

    def solve(self):
        for model in self.models_to_run:
            print('solving model')
            current_model = Model(name = model, args_dict=args_dict )
            self.solution = scipy.integrate.solve_ivp(
            fun=lambda t, y: current_model.subcut_rhs(t, y, current_model.args_dict['Q_p1'], 
                                current_model.args_dict['V_c'], current_model.args_dict['V_p1'], 
                                current_model.args_dict['CL'],
                                current_model.args_dict['X']),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=y0, t_eval=t_eval)

    def Plot(self):
        plt.plot(self.solution.t , self.solution.y[0])
        plt.show()
              
