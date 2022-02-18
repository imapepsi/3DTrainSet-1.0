import maya.cmds as mc
from TrainObject import Train


class CarTypeB(Train):

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * (7 / 8)
        lowerBoxPositionY = -(self._width * 1.5) + 0.5

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

    def _createBaseCar(self):
        octagon = 8

        self._base = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(self._base[0], offset=self._carBevel)

        lowerBox = self._createLowerCar()
        self._base = mc.polyBoolOp(self._base[0], lowerBox[0], op=1, n="body#")

        self._connectors()

        # Side circles
        startY = 0
        for y in range(startY, int(-self._height * 1/3), -2):
            increment = int(self._depth / 10)
            startZ = int((-self._depth / 2) + 2)
            for z in range(startZ, int(self._depth / 2), increment):
                circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, subdivisionsAxis=octagon, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(y, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)

        # Hangers of the lower compartment
        self._hangers()

    def _hangers(self):
        # Hangers of the lower compartment
        heightOfHanger = self._width + 2
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        octagon = 8
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=1, h=heightOfHanger, name="hangerCore#")
                rings = mc.polyCylinder(r=1.5, h=2, subdivisionsAxis=octagon, name="ring#")
                mc.move(-heightOfHanger/2, y=True, absolute=True)
                circleAndRing = mc.polyBoolOp(circles[0], rings[0], op=1, n="hangers#")
                mc.delete(circleAndRing[0], constructionHistory=True)
                mc.move(-self._height * 1/3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circleAndRing[0], op=1, n="baseTrainHR#")
                # Can't do a delete history here, not sure why
            count += 1
