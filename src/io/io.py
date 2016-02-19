#!/usr/bin/env python
#aimTool Developed in Prof. Yang's Research Group
import sys

def readStringStream():
    if not sys.stdin.isatty():
        outputString="";
        for line in sys.stdin:
            outputString += line;
        return outputString
    else:
        return None

if __name__ == "__main__":
    inputstr = readStringStream();
    sys.stdout.write(inputstr)
    #print inputstr
