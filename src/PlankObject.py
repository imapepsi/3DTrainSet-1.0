import maya.cmds as mc
from MayaObject import MayaObj


class Plank(MayaObj):
    def __init__(self, w=14, h=0.5, d=1.5):
        # width of planks = AxelLength-wheelCoreWidth + (offsetRailPlacement*2)
        self._names = []  # objName and node name
        self._width = w
        self._height = h
        self._depth = d

    def createPlank(self):
        """Create 1 plank"""
        p = mc.polyCube(w=self._width, h=self._height, d=self._depth, n="plank#")
        self._names = p

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getDepth(self):
        return self._depth


