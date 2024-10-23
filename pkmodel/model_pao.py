#
# Model class
#
# The idea is there will be an args_dict with all the parameters, including the name of the function?
# {'name': 'model1', 'Q_p1': 1.0, 'V_c': 1.0, 'V_p1': 1.0, 'CL': 1.0, 'X': 1.0, 'Dosing_Type': 'X'}
class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example parameter

    """
    def __init__(self, name , args_dict):
        self.name = name
        ### Check input parameters
        if args_dict["Dosing_Type"] not in ["Sub", "Bolus"]:
            raise ValueError("Unknown dosing type. Dosing types available are 'Sub' for subcutaneous and 'Bolus' for intravenous bolus.")
        
        self.args_dict = args_dict

    def add_dose_t_tophat_params(self, start_h, stop_h, duration_h, freq_h):
        if stop_h < start_h or stop_h == start_h:
            raise ValueError("Start time should be before the Stop time!")
        elif duration_h > freq_h:
            raise ValueError("Duration (h) should be shorter than or equal to (constant administration) the frequency of drug administration (h)")
        else:
            X_0 = self.args_dict['X']
            self.dose_t_tophat_params = [start_h, stop_h, duration_h, freq_h, X_0]

    def __str__(self):
        return self.name + ": Parameters are: " + str(self.args_dict)


## For small testing; to be deleted later
if __name__ == "__main__":
    import models
    model = Model(name = 'model1' , args_dict = models.model1)
    print(model)
    model.add_dose_t_tophat_params(10,100,1,1)
    print(model.dose_t_tophat_params)

    t_eval = np.linspace(0 , 1 , 100)
    y0 = np.array([0.0, 0.0])
    models_to_run = ['model1', 'model1']
    sol = Solution(models_to_run=models_to_run , t_eval=t_eval , y0=y0)
    sol.solve()






