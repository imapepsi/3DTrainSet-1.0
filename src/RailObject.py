import maya.cmds as mc
from MayaObject import MayaObj

class Rail(MayaObj):
    # Depth uses fence post problem based of plank attributes
    def __init__(self, depth):
        self._names = []  # objName and node name
        self._depth = depth
        self._coreW = 0.5
        self._coreH = 0.8
        self._TopW = 1.0
        self._BottomW = 1.5
        self._guardH = 0.2
        self._totalH = 1.0

    def createRail(self):
        """Create one rail"""
        # bottom
        bottom = mc.polyCube(w=self._BottomW, h=self._guardH, d=self._depth, n="railBottom#")
        mc.move(self._guardH/2, y=True, absolute=True)  # Move bottom to be level 0 by taking half the height upwards

        # core
        core = mc.polyCube(w=self._coreW, h=self._coreH, d=self._depth, n="railCore#")
        mc.move((self._coreH/2)+(self._guardH/2), y=True, absolute=True)  # Move core to be level 0 by taking half the height upwards (now it will overlap with bottom

        # top
        top = mc.polyCube(w=self._TopW, h=self._guardH, d=self._depth, n="railTop#")
        mc.move(self._coreH+(self._guardH/2), y=True, absolute=True)  # Move core to be overlap top of the core

        # Union objects
        # mc.select(d=True)  # Deselect another objects
        railBC = mc.polyBoolOp(core[0], bottom[0], op=1, n="railBC#")
        self._names = mc.polyBoolOp(railBC[0], top[0], op=1, n="rail#") # Pivot will be created at the bottom of the bottom peice

    def flipRail(self):
        """Flip rail upside down"""
        mc.select(self._names[0], r=True)
        mc.rotate(180, z=True, absolute=True)

    def getTopW(self):
        return self._TopW