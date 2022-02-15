import maya.cmds as mc
from MayaObject import MayaObj
from BoltObject import Bolt


class BoltSet(MayaObj):
    def __init__(self):
        self._names = []
        self._bolts = []

    def createSet(self, plankDepth, plankHeight):
        """Create 2 bolts and union"""
        boltLocZ = plankDepth/4
        boltLocY = plankHeight

        # Create 4 bolt objects
        for i in range(4):
            b = Bolt()
            b.createBolt()
            self._bolts.append(b)

        # Space out each bolt
        for i in range(4):
            b = self._bolts[i]
            mc.select(b.getName(), r=True)
            if i > 1:
                if i == 2:
                    boltLocZ = plankDepth/4  # Reset

                mc.rotate(180, z=True, absolute=True)  # Flip
                mc.move(-boltLocY, y=True, absolute=True)  # Move down

            mc.move(boltLocZ, z=True, absolute=True)  # Align on the plank
            boltLocZ = -boltLocZ

        # Union
        set1 = mc.polyBoolOp(self._bolts[0].getName(), self._bolts[1].getName(), op=1, name="boltAB")
        set2 = mc.polyBoolOp(self._bolts[2].getName(), self._bolts[3].getName(), op=1, name="boltBC")
        self._names = mc.polyBoolOp(set1[0], set2[0], op=1, name="boltSet")
        self.clearHistory()