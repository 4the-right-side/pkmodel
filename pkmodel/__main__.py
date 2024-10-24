import argparse
import numpy as np
from models import * ## importing all registered models
from pkmodel import Model, Protocol, Solution

parser = argparse.ArgumentParser(
        description = """ This is the programme that will help you solve ODEs to simulate how pharmacokinetics works!
        Please first check the parameters of the models in models.py to ensure this programme runs correctly.
        This programme will read the number of copies of the peripheral compartments, parameters for administering the drug, and the initial quantities of drugs inside the body. Parameters associated with the patient body (i.e. the model!) are in models.py.""",
        epilog = 'That is how you run this programme!')
parser.add_argument("-t_i", "--start_h", nargs = '?', default = 0, type = float,
                    help="start time [h]")
parser.add_argument("-t_f", "--stop_h", nargs = '?', default = 240, type = float,
                    help="stop time [h]")
parser.add_argument("-d", "--duration_h", nargs = '?', default = 24, type = float,
                    help="duration of the drug before it sharply drops from 'X' ng to 0 [h]. You might want to check what the X parameter in models.py")
parser.add_argument("-f", "--freq_h", nargs = '?', default = 24, type = float,
                    help="How many hours you want to wait after administering the drug each time? [h].")
parser.add_argument("-N", "--num_peripheral", nargs = '?', default = 0, type = int,
                    help="Number of the peripheral compartments [integer].")
parser.add_argument("-q_0_i", "--initial_subcutaneous_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_0 [ng].")
parser.add_argument("-q_c_i", "--initial_central_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_c [ng].")
parser.add_argument("-q_p1_i", "--initial_peripheral_drug_quantity", nargs = '?', default = 0.0, type = float,
                    help="This option specifies the initial value of q_p1 [ng].")
parser.add_argument("-m", "--model", nargs = '?', default = "model1", type = str,
                    help="This specifies which model in the models.py you want to run.")

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
    sol.solve()
    sol.Plot()
    

if __name__ == "__main__":
    main()
