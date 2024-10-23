#
# Model class
#
# The idea is there will be an args_dict with all the parameters, including the name of the function?
# {'name': 'model1', 'Q_p1': 1.0, 'V_c': 1.0, 'V_p1': 1.0, 'CL': 1.0, 'X': 1.0, 'Dosing_Type': 'X'}
class Model:
    """A Pharmokinetic (PK) model
    This is a class which defines a PK model parameters by parsing the parameters from a dictionary stored within models.py file.
    You also need to add the parameters for Dose(t) including the start and stop times for drug administration (h), duration (h) of each administration, and the frequency of administration (h).

    Parameters
    ----------

    name: string, mandatory
    args_dict: dictionary, mandatory, you need to import this from the models.py file.

    """
    def __init__(self, name , args_dict):
        self.name = name
        ### Check input parameters
        if args_dict["Dosing_Type"] not in ["Sub", "Bolus"]:
            raise ValueError("Unknown dosing type. Dosing types available are 'Sub' for subcutaneous and 'Bolus' for intravenous bolus.")
        
        self.args_dict = args_dict

    def add_dose_t_tophat_params(self, start_h, stop_h, duration_h, freq_h):
        """
        This function adds parameters to produce a tophat function to be used in creating a protocol.

        Parameters
        ----------
        start_h: float, mandatory, start time in hours.
        stop_h: float, mandatory, stop time in hours.
        duration_h: float, mandatory, duration of drug administration in hours.
        freq_h: float, mandatory, Frequency of drug administration in hours.

        """
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







