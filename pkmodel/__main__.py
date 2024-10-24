import argparse
parser = argparse.ArgumentParser(
        description = 'This is the programme that will help you solve ODEs to simulate how pharmacokinetics works!',
        epilog = 'That is how you run this programme!')
parser.add_argument(flags=["-t_i, --start_h"], nargs = 1, default = 0, type = float)
parser.add_argument(flags=["-t_f, --stop_h"], nargs = 1, default = 240, type = float)
parser.add_argument(flags=["-d, --duration_h"], nargs = 1, default = 24, type = float)
parser.add_argument(flags=["-f, --freq_h"], nargs = 1, default = 24, type = float)
parser.add_argument(flags=["-N, --num_peripheral"], nargs = 1, default = 0, type = int)
parser.add_argument(flags=["-m, --models"], nargs = 1, default = "models.py", type = str)


def main():
    args = parser.parse_args()
    print(args)
    

if __name__ == "__main__":
    main()
