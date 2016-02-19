#!/usr/bin/env python
from common import isInt


class Axis:
    x = 0.0
    y = 0.0
    z = 0.0

    def setXYZ(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def toString(self):
        return "  %.14f  %.14f  %.14f\n" % (self.x, self.y, self.z)

class Atom(Axis):
    element = None

    def setElement(self, element):
        self.element = element

    def toString(self):
        if self.element is not None:
            return "  %.14f  %.14f  %.14f %s\n" % (self.x, self.y, self.z, self.element)
        return "  %.14f  %.14f  %.14f\n" % (self.x, self.y, self.z)



class POSCAR:
    """
    POSCAR CLASS CAN BE COMBINED WITH PROTOTYPE AND ELEMENT
    """

    originProtoType = "ABO3\n1.000000\n3.94477368123351 0.00000000000000 0.00000000000000\n0.00000000000000 3.94477368123351 0.00000000000000\n0.00000000000000 0.00000000000000 3.94477368123351\n3 1 1\nDirect(5) [A3B1C1]\n0.00000000000000 0.50000000000000 0.50000000000000\n0.50000000000000 0.00000000000000 0.50000000000000\n0.50000000000000 0.50000000000000 0.00000000000000\n0.00000000000000 0.00000000000000 0.00000000000000\n0.50000000000000 0.50000000000000 0.50000000000000"
    elements = []
    atoms = []
    axises = []
    scaleFactor = 0.0
    dist = []
    title = ""
    coordSystem = ""
    atomNums = 0
    isPOSCAR53 = False
    isPOSCAR46Atoms = False

    def __init__(self, protoType, args):
        if protoType is not None:
            self.originProtoType = protoType
        if args["ATOMS"] is not None:
            self.elements = args["ATOMS"].strip().split(',')
            self.isPOSCAR46Atoms = True
        self.parseProtoTypeAndFillAtoms(args)


    def parseProtoTypeAndFillAtoms(self, args):
        lines = self.originProtoType.split("\n")
        self.title = lines[0]
        index = 1

        # SCALE FACTOR
        self.scaleFactor = float(lines[index])
        index += 1

        # AXISES PARSING
        for i in range(0, 3):
            coords = lines[index+i].strip().split()
            if len(coords) != 3:
                raise Exception("Axis does not contain 3 coordinates!")
            axis = Axis()
            axis.setXYZ(float(coords[0]), float(coords[1]), float(coords[2]))
            self.axises.append(axis)
        index += 3

        # DISTRIBUTION

        data = lines[index].strip().split()
        if not isInt(data[0]):
            self.elements = data
            self.isPOSCAR53 = True
            index += 1
        nums = lines[index].strip().split()
        index += 1
        for i in range(0, len(nums)):
            self.dist.append(int(nums[i]))
            self.atomNums += int(nums[i])

        # COORDINATE SYSTEM
        self.coordSystem = lines[index].strip()
        index += 1

        # ATOMS
        if len(self.elements) != len(self.dist) and self.atomNums != len(lines) - 7:
            raise Exception(
                "Invalid POSCAR since the atom numbers are not match: % vs %" % (self.atomNums, len(lines) - 7))

        for i in range(0, len(self.dist)):
            if self.isPOSCAR46Atoms:
                self.title += self.elements[i] + str(self.dist[i])
            for j in range(0, self.dist[i]):
                atom = Atom()
                coords = lines[index].strip().split()
                if len(coords) != 3 and len(coords) != 4:
                    raise Exception("Atom does not contain 3 coordinates!")
                atom.setXYZ(float(coords[0]), float(coords[1]), float(coords[2]))
                if self.isPOSCAR53 or self.isPOSCAR46Atoms:
                    atom.setElement(self.elements[i])
                index += 1
                self.atoms.append(atom)

        self.title += "\n"

    def generatePOSCAR(self, outputPath):
        res = self.title
        res += str(self.scaleFactor) + "\n"
        for i in range(0, 3):
            res += self.axises[i].toString()
        if self.isPOSCAR53:
            res += self.elements[0]
            for i in range(1, len(self.elements)):
                res += " %s" %self.elements[i]
            res += "\n"
        res += str(self.dist[0])
        for i in range(1, len(self.dist)):
            res += " %i" % self.dist[i]
        res += "\n"
        res += self.coordSystem + "\n"
        for i in range(0, len(self.atoms)):
            res += self.atoms[i].toString()
        if outputPath is None:
            print res
        else:
            file = open(outputPath, 'w')
            file.write(res)



