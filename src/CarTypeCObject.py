import maya.cmds as mc
from TrainObject import Train
import math


class CarTypeC(Train):
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

        rungWidth = railWidth + 0.5
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
