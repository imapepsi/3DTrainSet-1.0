import maya.cmds as mc
from MayaObject import MayaObj


class Bolt(MayaObj):
    def __init__(self):
        self._names = []
        self._boltR = 0.08
        self._boltH = 0.8
        self._nutR = 0.16  # boltR*2
        self._nutH = 0.20  # boltH/4

    def createBolt(self):
        """Create single bolt"""
        nutSubDiv = 8
        nutCenter = self._boltH/4

        body = mc.polyCylinder(radius=self._boltR, height=self._boltH, n="boltBody#")

        # Create the nut
        nut = mc.polyCylinder(radius=self._nutR, height=self._nutH, subdivisionsAxis=nutSubDiv, n="boltNut#")

        # Move the nut
        mc.move(nutCenter, y=True, absolute=True)  # Move the nut up on the bolt near the top

        # Union the objects
        mc.select(d=True)  # Deselect another objects
        # Pivot will be created at the center of the piece
        self._names = mc.polyBoolOp(body[0], nut[0], op=1, n="bolt#")
