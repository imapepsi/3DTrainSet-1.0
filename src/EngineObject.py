import maya.cmds as mc
from TrainObject import Train


class Engine(Train):

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height/2
        doorHeight = lowerHeight - 0.75

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=0.3)

        mc.move(-(lowerHeight*2), y=True, absolute=True)

        return lowerBox

    def createBaseCar(self):
        box = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(box[0], offset=0.3)

        lowerBox = self._createLowerCar()
        box = mc.polyBoolOp(box[0], lowerBox[0], op=1, n="body#")

        # End connector
        back = mc.polyPyramid(sideLength=self._width * (3 / 4), n="backPyramid#")
        mc.polyBevel(back[0], segments=5, offset=0.2)
        mc.select(back[0], r=True)
        mc.rotate(90, x=True, absolute=True)  # Order of rotations is important
        mc.rotate(45, z=True, absolute=True)
        mc.move((self._depth / 2) + 2.5, z=True, absolute=True)

        # No Front

        self._base = mc.polyBoolOp(box[0], back[0], op=1, n="baseEngineBody#")
        mc.delete(self._base[0], constructionHistory=True)

        # Side panels
        centerPanel = mc.polyCube(w=self._width + 1.0, h=self._height - 5.0, d=self._depth - 3.0, name="panel#")
        self._base = mc.polyBoolOp(self._base[0], centerPanel[0], op=1, n="baseTrainBodyCP#")

        # Side circle
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        for z in range(startZ, int(self._depth / 2), increment):
            circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, name="circle#")
            mc.rotate(90, z=True, absolute=True)
            mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
            self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
            count += 1

        # Hangers of the lower compartment
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        octagon = 8
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=1, h=self._width + 0.25, name="hangerCore#")
                rings = mc.polyCylinder(r=1.5, h=2, subdivisionsAxis=octagon, name="ring#")
                mc.move(-(self._width + 0.25) / 2, y=True, absolute=True)
                circles = mc.polyBoolOp(circles[0], rings[0], op=1, n="hangers#")
                mc.move(-self._height * 1 / 3, y=True, absolute=True)  # Shift down
                mc.move(z, z=True, absolute=True)
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainHR#")
            count += 1