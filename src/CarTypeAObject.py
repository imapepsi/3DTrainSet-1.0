import maya.cmds as mc
from TrainObject import Train


class CarTypeA(Train):
    def _createLowerCar(self):
        lowerWidth = self._width * (7/8)
        lowerHeight = self._height * (3/2)
        lowerBoxPositionY = -(lowerHeight - 1)

        cutHoleWidth = lowerWidth + 1.0  # +1 so we have a hole going through
        cutHoleHeight = lowerHeight - 3  # -3 gives a border on top
        cutHoleDepth = self._depth - 2  # -2 gives a border on sides

        barWidth = 1
        barDepth = 1

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=self._carBevel)

        cutHole = mc.polyCube(w=cutHoleWidth, h=cutHoleHeight, d=cutHoleDepth, name="cutHole#")
        lowerBox = mc.polyBoolOp(lowerBox[0], cutHole[0], op=2, n="lowerBodyBaseA#")

        # TODO(): Could just increment where I'm cutting
        # Build Bars for compartment
        # Add bolts on top???
        leftSidePositionX = lowerWidth/2-0.5
        rightSidePositionX = -lowerWidth/2+0.5
        startZ = int((-cutHoleDepth/2)+3)
        endZ = 9
        increment = 3
        for x in [leftSidePositionX, rightSidePositionX]:  # Left or Right edge of car
            for z in range(startZ, endZ, increment):
                bar = mc.polyCube(w=barWidth, h=cutHoleHeight, d=barDepth, name="bar#")
                mc.move(x, z, xz=True, absolute=True)
                lowerBox = mc.polyBoolOp(lowerBox[0], bar[0], op=1, n="lowerBodyBaseB#")

        mc.select(lowerBox[0], r=True)
        mc.move(lowerBoxPositionY, y=True, absolute=True)

        return lowerBox

    def _createUpperCar(self):
        self._base = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(self._base[0], offset=self._carBevel)

        # TODO(): Can't put these at the end of the function for some reason: car isn't even created
        lowerBox = self._createLowerCar()
        self._base = mc.polyBoolOp(self._base[0], lowerBox[0], op=1, n="body#")

        self._connectors()

        z = self._depth/4
        for side in [-1, 0, 1]:
            panel = mc.polyCube(w=self._width + 1.0, h=self._height / 3, d=4, name="panel#")
            if side != 0:  # Not the center panel
                mc.move(side*z, z=True, absolute=True)
            self._base = mc.polyBoolOp(self._base[0], panel[0], op=1, n="baseTrainSP#")
            mc.delete(self._base[0], constructionHistory=True)

        tubeRadius = 0.75
        tubeHeight = self._depth/2 + 3
        tubeSubDiv = 8  # Octagon Shape
        tubePosX = self._width/2
        tubePosY = -self._height/2 + tubeRadius*2 + 0.25

        for side in [-1, 1]:
            tube = mc.polyCylinder(r=tubeRadius, h=tubeHeight, subdivisionsAxis=tubeSubDiv, name="tube#")
            mc.move(tubePosX*side, tubePosY, xy=True, absolute=True)
            mc.rotate(90, x=True, absolute=True)
            self._base = mc.polyBoolOp(self._base[0], tube[0], op=1, n="body#")
            mc.delete(self._base[0], constructionHistory=True)

        # Hangers of the lower compartment
        self._hangers()

    def _hangers(self):
        # Hangers of the lower compartment
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        octagon = 8
        for z in range(startZ, int(self._depth / 2), increment):
            circles = mc.polyCylinder(r=1, h=self._width * (3/4), subdivisionsAxis=octagon, name="hangerCore#")
            mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
            self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainHR#")
            # Can't do a delete history here, not sure why
