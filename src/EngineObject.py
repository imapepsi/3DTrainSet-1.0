import maya.cmds as mc
import TrainObject

import importlib
importlib.reload(TrainObject)


class Engine(TrainObject.Train):

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height/2
        lowerBoxBevel = 0.3
        lowerBoxPositionY = -(lowerHeight*2)

        boxPanelWidth = lowerWidth-1
        boxPanelHeight = lowerHeight-1

        outerTubeRadius = lowerWidth / 2
        outerTubeHeight = self._depth
        innerTubeRadius = lowerWidth / 4
        innerTubeHeight = self._depth + 2
        innerTubeSubDiv = 8  # Octagon Shape
        ringRadius = outerTubeRadius + 0.2
        tubePositionY = -(lowerHeight * 3)

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=lowerBoxBevel)

        boxPanel = mc.polyCube(w=boxPanelWidth, h=boxPanelHeight, d=1, name="lowerBoxPanel#")
        mc.move(-self._depth, z=True, absolute=True)

        # Combine panel and lower box
        lowerBox = mc.polyBoolOp(lowerBox[0], boxPanel[0], op=2, n="lowerBox#")
        mc.move(lowerBoxPositionY, y=True, absolute=True)
        mc.delete(lowerBox[0], constructionHistory=True)

        innerTube = mc.polyCylinder(r=innerTubeRadius, h=innerTubeHeight, subdivisionsAxis=innerTubeSubDiv, name="innerTube#")
        outerTube = mc.polyCylinder(r=outerTubeRadius, h=outerTubeHeight, name="outerTube#")
        tube = mc.polyBoolOp(outerTube[0], innerTube[0], op=1, n="tube#")
        mc.delete(tube[0], constructionHistory=True)

        distBetweenRings = 2
        numRings = self._depth/distBetweenRings
        startY = -self._depth/2 + distBetweenRings
        for y in range(int(startY), int(numRings), distBetweenRings):
            ring = mc.polyTorus(r=ringRadius, n="ring#")
            mc.move(y, y=True, absolute=True)
            tube = mc.polyBoolOp(tube[0], ring[0], op=1, n="tube#")
            mc.delete(tube[0], constructionHistory=True)

        mc.select(tube[0], r=True)
        mc.rotate(90, x=True, absolute=True)  # Vertical to horizontal
        mc.move(tubePositionY, y=True, absolute=True)
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
