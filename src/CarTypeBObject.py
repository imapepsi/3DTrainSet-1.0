import maya.cmds as mc
from TrainObject import Train


class CarTypeB(Train):

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * (7 / 8)
        cutHoleDepth = self._depth - 2

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=0.3)

        cutHole = mc.polyCube(w=lowerWidth + 1.0, h=lowerHeight - 2, d=cutHoleDepth, name="cutHole#")
        lowerBox = mc.polyBoolOp(lowerBox[0], cutHole[0], op=2, n="lowerBodyBaseA#")

        mc.select(lowerBox[0], r=True)
        mc.move(-(self._width * 1.25) - 1, y=True, absolute=True)

        return lowerBox
