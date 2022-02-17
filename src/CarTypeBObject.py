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

    def createBaseCar(self):
        octagon = 8

        box = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(box[0], offset=0.3)

        lowerBox = self._createLowerCar()
        box = mc.polyBoolOp(box[0], lowerBox[0], op=1, n="body#")

        # Ends/Connectors
        pyramids = []
        for factor in [-1, 1]:
            pyramid = mc.polyPyramid(sideLength=self._width*(3/4), n="pyramid#")
            mc.polyBevel(pyramid[0], segments=5, offset=0.2)
            mc.select(pyramid[0], r=True)
            mc.rotate(factor*90, x=True, absolute=True)  # Order of rotations is important
            mc.rotate(45, z=True, absolute=True)
            mc.move((factor*self._depth/2) + (factor*2.5), z=True, absolute=True)  # 2.5 gives nice edge around it
            pyramids.append(pyramid)

        self._base = mc.polyBoolOp(box[0], pyramids[0][0], op=1, n="bodyBaseA#")
        self._base = mc.polyBoolOp(self._base[0], pyramids[1][0], op=1, n="baseTrainBody#")
        mc.delete(self._base[0], constructionHistory=True)

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
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=1, h=self._width + 0.25, name="hangerCore#")
                rings = mc.polyCylinder(r=1.5, h=2, subdivisionsAxis=octagon, name="ring#")
                mc.move(-(self._width + 0.25) / 2, y=True, absolute=True)
                circleAndRing = mc.polyBoolOp(circles[0], rings[0], op=1, n="hangers#")
                mc.delete(circleAndRing[0], constructionHistory=True)
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circleAndRing[0], op=1, n="baseTrainHR#")
                # Can't do a delete history here, not sure why
            count += 1