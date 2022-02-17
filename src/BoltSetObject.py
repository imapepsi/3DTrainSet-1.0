import maya.cmds as mc
from MayaObject import MayaObj
from BoltObject import Bolt


class BoltSet(MayaObj):
    def __init__(self):
        self._names = []
        self._bolts = []
        self._numBolts = 4

    def createSet(self, plankDepth, plankHeight):
        """Create 2 bolts and union"""
        boltLocStartZ = plankDepth/4
        boltLocZ = boltLocStartZ
        boltLocY = plankHeight

        # Create 4 bolt objects
        for i in range(self._numBolts):
            b = Bolt()
            b.createBolt()
            if i > 1:
                if i == 2:
                    boltLocZ = boltLocStartZ  # Reset

                mc.rotate(180, z=True, absolute=True)  # Flip
                mc.move(-boltLocY, y=True, absolute=True)  # Move down

            mc.move(boltLocZ, z=True, absolute=True)  # Align on the plank
            boltLocZ = -boltLocZ
            self._bolts.append(b)

        # Union
        set1 = mc.polyBoolOp(self._bolts[0].getName(), self._bolts[1].getName(), op=1, name="boltAB")
        set2 = mc.polyBoolOp(self._bolts[2].getName(), self._bolts[3].getName(), op=1, name="boltBC")
        self._names = mc.polyBoolOp(set1[0], set2[0], op=1, name="boltSet")
        self.clearHistory()
