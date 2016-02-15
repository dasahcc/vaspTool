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
    element = ""

    def setElement(self, element):
        self.element = element

    def toString(self):
        return "  %.14f  %.14f  %.14f %s\n" % (self.x, self.y, self.z, self.element)



class POSCAR:
    """
    POSCAR CLASS CAN BE COMBINED WITH PROTOTYPE AND ELEMENT
    """

    originProtoType = "ABO3\n1.000000\n3.94477368123351 0.00000000000000 0.00000000000000\n0.00000000000000 3.94477368123351 0.00000000000000\n0.00000000000000 0.00000000000000 3.94477368123351\n3 1 1\nDirect(5) [A3B1C1]\n0.00000000000000 0.50000000000000 0.50000000000000\n0.50000000000000 0.00000000000000 0.50000000000000\n0.50000000000000 0.50000000000000 0.00000000000000\n0.00000000000000 0.00000000000000 0.00000000000000\n0.50000000000000 0.50000000000000 0.50000000000000"
    originAtoms = ""
    atoms = []
    axises = []
    scaleFactor = 0.0
    dist = []
    title = ""
    coordSystem = ""
    atomNums = 0

    def __init__(self, prototypeFile, atoms):
        if prototypeFile is not None:
            sourceFile = open(prototypeFile, 'r')
            self.originProtoType = sourceFile.read()
        self.originAtoms = atoms
        self.parseProtoTypeAndFillAtoms()


    def parseProtoTypeAndFillAtoms(self):
        lines = self.originProtoType.split("\n")

        # SCALE FACTOR
        self.scaleFactor = float(lines[1])

        # AXISES PARSING
        for i in range(2, 5):
            coords = lines[i].strip().split()
            if len(coords) != 3:
                raise Exception("Axis does not contain 3 coordinates!")
            axis = Axis()
            axis.setXYZ(float(coords[0]), float(coords[1]), float(coords[2]))
            self.axises.append(axis)

        # DISTRIBUTION
        nums = lines[5].strip().split()
        for i in range(0, len(nums)):
            self.dist.append(int(nums[i]))
            self.atomNums += int(nums[i])

        # COORDINATE SYSTEM
        self.coordSystem = lines[6].strip()

        # ATOMS
        elements = self.originAtoms.strip().split(',')
        if len(elements) != len(self.dist) and self.atomNums != len(lines) - 7:
            raise Exception(
                "Invalid POSCAR since the atom numbers are not match: % vs %" % (self.atomNums, len(lines) - 7))
        index = 7
        for i in range(0, len(elements)):
            self.title += elements[i] + str(self.dist[i])
            for j in range(0, self.dist[i]):
                atom = Atom()
                coords = lines[index].strip().split()
                if len(coords) != 3 and len(coords) != 4:
                    raise Exception("Atom does not contain 3 coordinates!")
                atom.setXYZ(float(coords[0]), float(coords[1]), float(coords[2]))
                atom.setElement(elements[i])
                index += 1
                self.atoms.append(atom)

        self.title += "\n"

    def generatePOSCAR(self, outputPath):
        res = self.title
        res += str(self.scaleFactor) + "\n"
        for i in range(0, 3):
            res += self.axises[i].toString()
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



