#!/opt/local/bin/python
#vaspTool Developed in Prof. Yang's Research Group
import sys

def readStringStream():
    outputString="";
    for line in sys.stdin:
        outputString += line;
    return outputString

if __name__ == "__main__":
    inputstr = readStringStream();
    sys.stdout.write(inputstr)
    #print inputstr
