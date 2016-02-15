#!/opt/local/bin/python
#vaspTool Developed in Prof. Yang's Research Group
import argparse
#import io
from POSCAR import POSCAR
from io import readStringStream

def executeFunction(args):
    if not args["poscar"]:
        if args["ATOMS"] is None:
            raise Exception("Invalid argument \"ATOMS\": no atoms found!")
        data = readStringStream()

        if args["STRUCTURE"] is not None:
            prototype = open(args["STRUCTURE"], 'r')
            data = prototype.read()
        poscar = POSCAR(data, args["ATOMS"])

        poscar.generatePOSCAR(args["OUTPUTPATH"])
    if args["ABCCAR"]:
        xstructure=readStringStream()
        print xstructure



def main():
    parser = argparse.ArgumentParser(description = "Command line python tool for dealing with VASP data.\n")

    
    # POSCAR PRODUCE COMMAND
    parser.add_argument("-abccar","--ABCCAR", help="Read a POSCAR and convert it as abccar format", default=False, required=False, action="store_true")

    parser.add_argument("-pos", "--poscar", help="Generate POSCAR from prototypes", default=True, required=False, action="store_false")
    parser.add_argument("-sc", "--STRUCTURE", help="Structure used for generating POSCAR", required=False)
    parser.add_argument("-ats", "--ATOMS", help="Atoms to fill in the structure", required=False)
    parser.add_argument("-pwf", "--OUTPUTPATH", help="Output path of the data", default=None, required=False)


    args = vars(parser.parse_args())
    executeFunction(args)

if __name__ == "__main__":
    main()
