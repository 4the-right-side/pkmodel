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
        self.dose_t = 1.0

    def __str__(self):
        return self.name + ": Parameters are: " + str(self.args_dict)


## For small testing; to be deleted later
if __name__ == "__main__":
    import models
    model = Model(name = 'model1' , args_dict = models.model1)
    print(model)







