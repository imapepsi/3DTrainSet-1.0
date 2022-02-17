import maya.cmds as mc
from MayaObject import MayaObj
from math import pi


class Wire(MayaObj):
    def __init__(self, railHeight=1, plankHeight=0.5, largeRadius=4, mediumRadius=2):
        # Medium radius = half of large
        self._names = []
        self._wheelSet = []
        self._radius = 0.5
        self._bendRadius = (railHeight*2) + plankHeight + largeRadius + mediumRadius
        # Self._height: + 1, to give a tiny gap for track to fit between wheels
        self._height = ((((railHeight*2) + plankHeight + largeRadius + mediumRadius) * pi) / 2) + 1
        self._subdivisions = 30
        self._curve = 90  # Half circle

    def createWire(self):
        self._names = mc.polyCylinder(r=self._radius, h=self._height, subdivisionsHeight=self._subdivisions, name="cord#")
        wireBend = mc.nonLinear(type="bend", curvature=self._curve)
        self.clearHistory() # Maintain bend

    def getBendRadius(self):
        return self._bendRadius
