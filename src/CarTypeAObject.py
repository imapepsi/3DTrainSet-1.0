import maya.cmds as mc
from TrainObject import Train


class CarTypeA(Train):
    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * 1.5
        cutHoleDepth = self._depth-2

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=0.3)

        cutHole = mc.polyCube(w=lowerWidth + 1.0, h=lowerHeight-3, d=cutHoleDepth, name="cutHole#")
        lowerBox = mc.polyBoolOp(lowerBox[0], cutHole[0], op=2, n="lowerBodyBaseA#")

        startZ = int((-cutHoleDepth/2)+3)
        increment = 3
        for x in [lowerWidth/2-0.5, -lowerWidth/2+0.5]:
            for z in range(startZ, 9, increment):
                bar = mc.polyCube(w=1.0, h=lowerHeight-3, d=1.0, name="cutHole#")
                mc.move(x, z, xz=True, absolute=True)
                lowerBox = mc.polyBoolOp(lowerBox[0], bar[0], op=1, n="lowerBodyBaseB#")

        mc.select(lowerBox[0], r=True)
        mc.move(-(lowerHeight - 1), y=True, absolute=True)

        return lowerBox

    def createBaseCar(self):
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

# TODO(): Keep Fixing
        increment = int(self._depth / 2)
        startZ = int((-self._depth / 2) + 4)
        for z in range(startZ, int(self._depth / 2), increment):
            panel = mc.polyCube(w=self._width + 1.0, h=self._height / 3, d=4, name="panel#")
            mc.move(z, z=True, absolute=True)
            self._base = mc.polyBoolOp(self._base[0], panel[0], op=1, n="baseTrainSP#")
            mc.delete(self._base[0], constructionHistory=True)

        # Hangers of the lower compartment
        self._hangers()

    def _hangers(self):
        # Hangers of the lower compartment
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        octagon = 8
        for z in range(startZ, int(self._depth / 2), increment):
                circles = mc.polyCylinder(r=1, h=self._width* (3/4), subdivisionsAxis=octagon, name="hangerCore#")
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainHR#")
                # Can't do a delete history here, not sure why
