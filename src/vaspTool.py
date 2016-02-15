#!/opt/local/bin/python
import argparse
from POSCAR import POSCAR

def executeFunction(args):
    if args["POSCAR"]:
        poscar = POSCAR(args["STRUCTURE"], args["ATOMS"])
        poscar.generatePOSCAR(args["OUTPUTPATH"])


def main():
    parser = argparse.ArgumentParser(description = "Command line python tool for dealing with VASP data.\n")

    # POSCAR PRODUCE COMMAND
    parser.add_argument("-pos", "--POSCAR", help="Generate POSCAR from prototypes", default=False, required=False)

    parser.add_argument("-sc", "--STRUCTURE", help="Structure used for generating POSCAR", default=None, required=False)
    parser.add_argument("-ats", "--ATOMS", help="Atoms to fill in the structure", required=False)

    parser.add_argument("-pwf", "--OUTPUTPATH", help="Output path of the data", default=None, required=False)
    args = vars(parser.parse_args())
    executeFunction(args)

if __name__ == "__main__":
    main()
