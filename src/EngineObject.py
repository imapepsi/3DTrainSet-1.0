import maya.cmds as mc
import TrainObject

import importlib
importlib.reload(TrainObject)


class Engine(TrainObject.Train):

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height/2

        lowerBoxPanel = mc.polyCube(w=lowerWidth-1, h=lowerHeight-1, d=1, name="lowerBoxPanel#")
        mc.move(-self._depth, z=True, absolute=True)

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=0.3)

        lowerBox = mc.polyBoolOp(lowerBox[0], lowerBoxPanel[0], op=2, n="lowerBox#")
        mc.move(-(lowerHeight*2), y=True, absolute=True)
        mc.delete(lowerBox[0], constructionHistory=True)

        octagon = 8
        innerTube = mc.polyCylinder(r=lowerWidth / 4, h=self._depth+2, subdivisionsAxis=octagon, name="innerTube#")
        outerTube = mc.polyCylinder(r=lowerWidth / 2, h=self._depth, name="outerTube#")
        tube = mc.polyBoolOp(outerTube[0], innerTube[0], op=1, n="tube#")
        mc.delete(tube[0], constructionHistory=True)

        distBetweenRings = 2
        numRings = self._depth/distBetweenRings
        startY = -self._depth/2 + distBetweenRings
        for y in range(int(startY), int(numRings), distBetweenRings):
            ring = mc.polyTorus(r=(lowerWidth/2) + 0.2, tw=0.5)
            mc.move(y, y=True, absolute=True)
            tube = mc.polyBoolOp(tube[0], ring[0], op=1, n="tube#")
            mc.delete(tube[0], constructionHistory=True)

        mc.rotate(90, x=True, absolute=True)
        mc.move(-(lowerHeight * 3), y=True, absolute=True)
        mc.delete(tube[0], constructionHistory=True)

        lowerCompartment = mc.polyBoolOp(lowerBox[0], tube[0], op=1, n="lowerCompartment#")

        return lowerCompartment

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
        self._hangers()
