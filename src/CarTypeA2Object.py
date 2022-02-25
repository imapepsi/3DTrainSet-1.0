import maya.cmds as mc
from TrainObject import Train

# Mix of Default and TypeB
# Default Upper and TypeA Lower


class CarTypeA2(Train):
    def _createLowerCar(self):
        print("Create my A2")
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
        lowerBox = mc.polyBoolOp(lowerBox[0], cutHole[0], op=2, n="lowerBodyBase#")
        # DON't Set objects equal to polyBoolOp?????
        print(lowerBox)

        # Add bolts on top???
        leftSidePositionX = lowerWidth/2-0.5
        rightSidePositionX = -lowerWidth/2+0.5
        startZ = int((-cutHoleDepth/2)+3)
        endZ = 9
        increment = 3
        emptyList = []
        for x in [leftSidePositionX, rightSidePositionX]:  # Left or Right edge of car
            for z in range(startZ, endZ, increment):
                bar = mc.polyCube(w=barWidth, h=cutHoleHeight, d=barDepth, name="bar#")
                mc.move(x, z, xz=True, absolute=True)
                emptyList.append(bar[0])

        lowerBox = mc.group(emptyList, lowerBox[0])  #Can't do multiple polyBoolop???
        print(lowerBox)

        mc.select(lowerBox, r=True)
        mc.move(lowerBoxPositionY, y=True, absolute=True)

        return lowerBox

    # TODO(): Why is the rest of the movement of the cars off now?