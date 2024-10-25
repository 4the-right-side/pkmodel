import argparse
import numpy as np
from pkmodel import *

parser = argparse.ArgumentParser(
        description = "PKModel software By 4The-right-side Team!   ---------------  Contributors: Anita Applegarth, Callum Houghton-Flory, Edward Wheeler, Nichakorn Pipatpadungsin (Pao).  This is the programme that will help you solve ODEs to simulate how pharmacokinetics works! Please first check the parameters of the models in models.py to ensure this programme runs correctly. This programme will read the number of copies of the peripheral compartments, parameters for administering the drug, and the initial quantities of drugs inside the body. Parameters associated with the patient body (i.e. the model!) are in models.py.",
        epilog = 'PKModel will output the .npz (compressed numpy array) containing the raw results, and .png for the plot for analysis.')
parser.add_argument("-t_i", "--start_h", nargs = '?', default = 0, type = float,
                    help="start time [h] Default value = 0.0 h")
parser.add_argument("-t_f", "--stop_h", nargs = '?', default = 240, type = float,
                    help="stop time [h] Default value = 240.0 h")
parser.add_argument("-d", "--duration_h", nargs = '?', default = 24, type = float,
                    help="duration of the drug before it sharply drops from 'X' ng to 0 [h]. You might want to check what the X parameter in models.py. Default value = 24 h")
parser.add_argument("-f", "--freq_h", nargs = '?', default = 24, type = float,
                    help="How many hours you want to wait after administering the drug each time? [h] Default value = 24 h.")
parser.add_argument("-N", "--num_peripheral", nargs = '?', default = 0, type = int,
                    help="Number of the peripheral compartments [integer] Default value = 0.")
parser.add_argument("-q_0_i", "--initial_subcutaneous_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_0 [ng]. Default value = 0.0.")
parser.add_argument("-q_c_i", "--initial_central_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_c [ng]. Default value = 0.0")
parser.add_argument("-q_p1_i", "--initial_peripheral_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_p1 [ng]. Default value = 0.0")
parser.add_argument("-m", "--model", nargs = '?', default = "model1", type = str,
                    help="This specifies which model in the models.py you want to run. Currently we have model1 =  Intravenous Bolus and model2 = Subcutaneous model. Default value = model1")

def main():
    ## Setting up the variables
    registered_models = { "model1": model1,
                         "model2": model2 }
    args = parser.parse_args()
    t_eval = np.linspace(args.start_h, args.stop_h, 1000) ## 1000 timesteps should be fine
    y0 = np.array([args.initial_subcutaneous_drug_quantity, 
                   args.initial_central_drug_quantity, 
                   args.initial_peripheral_drug_quantity])
    model = registered_models[args.model]
    ## Running the programme
    sol = Solution(args_dict = model, t_eval = t_eval , y0 = y0)
    sol.define_peripheral_compartments(args.num_peripheral)
    sol.solve(start_h = args.start_h,
              stop_h = args.stop_h,
              duration_h = args.duration_h,
              freq_h = args.freq_h)
    sol.Plot()
    

if __name__ == "__main__":
    main()
