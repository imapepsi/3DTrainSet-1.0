import maya.cmds as mc
from CarTypeCObject import CarTypeC

import math

# Upper B and lower C

class CarTypeC2(CarTypeC):
    def _createUpperCar(self):

        octagon = 8

        self._base = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(self._base[0], offset=self._carBevel)

        self._connectors()

        # Side circles
        height = self._width + 0.50
        startY = 2
        y = startY
        for rows in range(4):
            startZ = int((-self._depth / 2) + 2)
            z = startZ
            radius = 0.5
            for column in range(9):
                circles = mc.polyCylinder(r=radius, h=height, subdivisionsAxis=octagon, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(y, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)
                z += self._depth / 10
            y -= 1.75

        print("new code")
        newHeight = height + 0.7
        startY = 2
        y = startY
        radius = 0.4
        for rows in range(4):
            startZ = int((-self._depth / 2) + 2)
            z = startZ
            for column in range(9):
                circles = mc.polyCylinder(r=radius, h=newHeight, subdivisionsAxis=octagon, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(y, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)
                z += self._depth / 10
            y -= 1.75
            radius -= 0.05

        print("end new code")

        # Hangers of the lower compartment
        self._hangers()

        lowerBox = self._createLowerCar()
        self._base = mc.polyBoolOp(self._base[0], lowerBox[0], op=1, n="body#")