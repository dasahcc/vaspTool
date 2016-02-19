#!/opt/local/bin/python
#vaspTool Developed in Prof. Yang's Research Group
import argparse
from io import readStringStream
from POSCAR import POSCAR

def executeFunction(args):
    if not args["poscar"]:
        data = readStringStream()
        if args["STRUCTURE"] is not None:
            prototype = open(args["STRUCTURE"], 'r')
            data = prototype.read()
        poscar = POSCAR(data, args)

        poscar.generatePOSCAR(args["OUTPUTPATH"])
    if args["abccar"]:
        xstructure=readStringStream()
        print xstructure



def main():
    parser = argparse.ArgumentParser(description = "Command line python tool for dealing with VASP data.\n")
    
    # POSCAR PRODUCE COMMAND
    parser.add_argument("-abc","--abccar", help="Read a POSCAR and convert it as abccar format", default=False, required=False, action="store_true")

    parser.add_argument("-pos", "--poscar", help="Generate POSCAR from prototypes", default=True, required=False, action="store_false")
    parser.add_argument("-sc", "--STRUCTURE", help="Structure used for generating POSCAR", required=False)
    parser.add_argument("-ats", "--ATOMS", help="Atoms to fill in the structure", required=False)
    parser.add_argument("-pwf", "--OUTPUTPATH", help="Output path of the data", default=None, required=False)


    print "parser.parse_args()", parser.parse_args()
    args = vars(parser.parse_args())
    print "args are", args
    print 'args.abccar', args["abccar"]
    executeFunction(args)

if __name__ == "__main__":
    main()
