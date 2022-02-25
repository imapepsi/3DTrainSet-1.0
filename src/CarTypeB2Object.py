import maya.cmds as mc
from TrainObject import Train

# Mix of Default and TypeB
# Default Upper and TypeB Lower


class CarTypeB2(Train):
    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * (7 / 8)
        lowerBoxPositionY = -(self._width * 1.25) - 1

        cutHoleWidth = lowerWidth + 1.0
        cutHoleHeight = lowerHeight - 2
        cutHoleDepth = self._depth - 2

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=self._carBevel)

        cutHole = mc.polyCube(w=cutHoleWidth, h=cutHoleHeight, d=cutHoleDepth, name="cutHole#")
        lowerBox = mc.polyBoolOp(lowerBox[0], cutHole[0], op=2, n="lowerBodyBaseA#")

        mc.select(lowerBox[0], r=True)
        mc.move(lowerBoxPositionY, y=True, absolute=True)

        return lowerBox
