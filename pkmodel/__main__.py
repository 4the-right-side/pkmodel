import argparse
parser = argparse.ArgumentParser(
        description = 'This is the programme that will help you solve ODEs to simulate how pharmacokinetics works!',
        epilog = 'That is how you run this programme!')
parser.add_argument("-t_i", "--start_h", nargs = 1, default = 0, type = float,
                    help="start time [h]")
parser.add_argument("-t_f", "--stop_h", nargs = 1, default = 240, type = float,
                    help="stop time [h]")
parser.add_argument("-d", "--duration_h", nargs = 1, default = 24, type = float,
                    help="duration of the drug before it sharply drops from 'X' ng to 0 [h]. You might want to check what the X parameter in models.py")
parser.add_argument("-f", "--freq_h", nargs = 1, default = 24, type = float,
                    help="How many hours you want to wait after administering the drug each time? [h].")
parser.add_argument("-N", "--num_peripheral", nargs = 1, default = 0, type = int,
                    help="Number of the peripheral compartments [integer].")
parser.add_argument("-m", "--models", nargs = 1, default = "models.py", type = str,
                    help="This option specifies the location of models.py.")


def main():
    args = parser.parse_args()
    print(args)
    

if __name__ == "__main__":
    main()
