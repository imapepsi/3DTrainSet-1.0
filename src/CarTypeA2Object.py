# This code doesn't work, too much effort
"""
import maya.cmds as mc
from TrainObject import Train

# Mix of Default and TypeB
# Default Upper and TypeA Lower


class CarTypeA2(Train):
    def _createUpperCar(self):
        baseOpNames = []

        baseOpNames.append(mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#"))
        mc.polyBevel(baseOpNames[-1], offset=self._carBevel)

        self._base = baseOpNames[-1]  # Must be assigned for connectors function
        self._connectors()

        # Side panels
        centerPanel = mc.polyCube(w=self._width + 1.0, h=self._height - 1, d=4.0, name="panel#")
        # Once a name is used in a polybool op maya looses track
        baseOpNames.append(mc.polyBoolOp(self._base[0], centerPanel[0], op=1, n="baseTrainBodyCP#"))
        mc.delete(baseOpNames[-1], constructionHistory=True)

        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        for z in range(startZ, int(self._depth / 2), increment):
            panel = mc.polyCube(w=self._width + 1.0, h=self._height / 3, d=1, name="panel#")
            mc.move(z, z=True, absolute=True)
            baseOpNames.append(mc.polyBoolOp(baseOpNames[-1][0], panel[0], op=1, n="baseTrainSP#"))
            mc.delete(baseOpNames[-1], constructionHistory=True)

        # Center circle
        circles = mc.polyCylinder(h=self._width + 2, name="circle#")
        mc.rotate(90, z=True, absolute=True)
        baseOpNames.append(mc.polyBoolOp(baseOpNames[-1][0], circles[0], op=1, n="baseTrainCC#"))
        mc.delete(baseOpNames[-1], constructionHistory=True)

        # Side circle
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                baseOpNames.append(mc.polyBoolOp(baseOpNames[-1][0], circles[0], op=1, n="baseTrainC#"))
            count += 1

        # Hangers of the lower compartment
        self._hangers()

        print("Create lowerCar")
        lowerBox = self._createLowerCar()

        print("Bool lower and upper")
        print(baseOpNames[-1][0])
        print(lowerBox[0])
        finalBase = mc.polyBoolOp(baseOpNames[-1][0], lowerBox[0], op=1, n="body#")
        print(finalBase)
        self._base = finalBase

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
        # DON't Set objects equal to polyBoolOp?????

        # Add bolts on top???
        leftSidePositionX = lowerWidth/2-0.5
        rightSidePositionX = -lowerWidth/2+0.5
        startZ = int((-cutHoleDepth/2)+3)
        endZ = 9
        increment = 3
        lowerBoxBars = []
        for z in range(startZ, endZ, increment):
            bar = mc.polyCube(w=barWidth, h=cutHoleHeight, d=barDepth, name="bar#")
            mc.move(rightSidePositionX, z, xz=True, absolute=True)
            if z == startZ:
                lowerBoxBars.append(mc.polyBoolOp(lowerBox[0], bar[0], op=1, n="lowerBodyBaseB#"))
            else:
                lowerBoxBars.append(mc.polyBoolOp(lowerBoxBars[-1][0], bar[0], op=1, n="lowerBodyBaseB#"))

        for z in range(startZ, endZ, increment):
            bar = mc.polyCube(w=barWidth, h=cutHoleHeight, d=barDepth, name="bar#")
            mc.move(leftSidePositionX, z, xz=True, absolute=True)
            if z == startZ:
                lowerBoxBars.append(mc.polyBoolOp(lowerBoxBars[-1][0], bar[0], op=1, n="lowerBodyBaseB#"))
            else:
                lowerBoxBars.append(mc.polyBoolOp(lowerBoxBars[-1][0], bar[0], op=1, n="lowerBodyBaseB#"))

        lowerBoxFinal = lowerBoxBars[-1]
        mc.select(lowerBoxFinal, r=True)
        mc.move(lowerBoxPositionY, y=True, absolute=True)

        return lowerBoxFinal
"""
