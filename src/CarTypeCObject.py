import maya.cmds as mc
from TrainObject import Train
import math


class CarTypeC(Train):
    def _createUpperCar(self):
        self._base = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(self._base[0], offset=self._carBevel)

        self._connectors()

        # Side panels
        centerPanel = mc.polyCube(w=self._width + 1.0, h=self._height - 1, d=4.0, name="panel#")
        self._base = mc.polyBoolOp(self._base[0], centerPanel[0], op=1, n="baseTrainBodyCP#")
        mc.delete(self._base[0], constructionHistory=True)

        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        for z in range(startZ, int(self._depth / 2), increment):
            panel = mc.polyCube(w=self._width + 1.0, h=self._height / 3, d=1, name="panel#")
            mc.move(z, z=True, absolute=True)
            self._base = mc.polyBoolOp(self._base[0], panel[0], op=1, n="baseTrainSP#")
            mc.delete(self._base[0], constructionHistory=True)

        # Center circle
        circles = mc.polyCylinder(h=self._width + 2, name="circle#")
        mc.rotate(90, z=True, absolute=True)
        self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainCC#")
        mc.delete(self._base[0], constructionHistory=True)

        # Side circle
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)
            count += 1

        # Hangers of the lower compartment
        self._hangers()

        lowerBox = self._createLowerCar()
        self._base = mc.polyBoolOp(self._base[0], lowerBox[0], op=1, n="body#")

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * (7 / 8)
        lowerBoxPositionY = -(self._width * 1.25) - 1

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=self._carBevel)

        lowerBox = self._createLadder(lowerBox)

        mc.select(lowerBox[0], r=True)
        mc.move(lowerBoxPositionY, y=True, absolute=True)

        return lowerBox

    def _createLadder(self, box):
        railWidth = self._width + 0.5
        railHeight = self._height - 3  # Should be 7, Height should always be an odd number for rung count
        railDepth = 1
        railPosZ = 2
        railPosX = self._width * (7/8) / 2

        rungWidth = railWidth
        rungHeight = 0.5
        rungDepth = railPosZ*2
        rungPosX = railPosX

        ladderPosZ = rungDepth + 2

        for l in range(4):
            # Rungs
            numRungs = railHeight - 1
            rungPosY = (railHeight/2) - (rungHeight*2)
            rungs = mc.polyCube(w=rungWidth, h=rungHeight, d=rungDepth, name="ladderRung#")
            mc.move(rungPosY, y=True, absolute=True)
            for r in range(numRungs):
                rung = mc.polyCube(w=rungWidth, h=rungHeight, d=rungDepth, name="ladderRung#")
                mc.move(rungPosY, y=True, absolute=True)
                rungs = mc.polyBoolOp(rungs[0], rung[0], op=1, name="baseTrainLRR#")
                rungPosY = rungPosY - (rungHeight*2)

            ladder = rungs

            # Rails
            for side in [-1, 1]:
                ladderRail = mc.polyCube(w=railWidth, h=railHeight, d=railDepth, name="ladderRail#")
                mc.move(railPosZ*side, z=True, absolute=True)
                ladder = mc.polyBoolOp(ladder[0], ladderRail[0], op=1, name="baseTrainLR#")

            mc.select(ladder[0], r=True)
            mc.move(ladderPosZ, z=True, absolute=True)
            ladderPosZ -= rungDepth

            box = mc.polyBoolOp(box[0], ladder[0], op=1, name="baseTrainLadder#")

        return box
