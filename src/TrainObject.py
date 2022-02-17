import maya.cmds as mc
from MayaObject import MayaObj
from WheelSetObject import WheelSet
from WireObject import Wire


class Train(MayaObj):
    def __init__(self, w=10, h=10, d=20):
        self._names = []
        self._wheelSets = []  # List of Wheel objs
        self._wires = []  # List of Wire Objects
        self._base = []  # Name of base obj
        self._width = w
        self._height = h
        self._depth = d

    def _createLowerCar(self):
        lowerWidth = self._width * (7 / 8)
        lowerHeight = self._height * (7 / 8)
        doorHeight = lowerHeight - 0.75

        lowerBox = mc.polyCube(w=lowerWidth, h=lowerHeight, d=self._depth, name="lowerBodyBase#")
        mc.polyBevel(lowerBox[0], offset=0.3)

        doorR = mc.polyCube(w=lowerWidth + 1.0, h=lowerHeight * (3 / 4), d=self._depth * (1 / 3), name="doorR#")
        mc.move(self._depth * (1 / 3) / 2, z=True, absolute=True)
        mc.polyBevel(doorR[0], offset=0.2)
        doorL = mc.polyCube(w=lowerWidth + 1.0, h=lowerHeight * (3 / 4), d=self._depth * (1 / 3), name="doorL#")
        mc.move(-self._depth * (1 / 3) / 2, z=True, absolute=True)
        mc.polyBevel(doorL[0], offset=0.2)
        door = mc.polyBoolOp(doorR[0], doorL[0], op=1, n="doors#")

        lowerBox = mc.polyBoolOp(lowerBox[0], door[0], op=1, n="lowerBodyBaseA#")
        mc.move(-(self._width * 1.25) - 1, y=True, absolute=True)

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

        # Side panels
        centerPanel = mc.polyCube(w=self._width + 1.0, h=self._height - 1, d=4.0, name="panel#")
        self._base = mc.polyBoolOp(self._base[0], centerPanel[0], op=1, n="baseTrainBodyCP#")
        mc.delete(self._base[0], constructionHistory=True)

        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        for z in range(startZ, int(self._depth / 2), increment):
            panel = mc.polyCube(w=self._width + 1.0, h=self._height / 3, d=1, name="panel#")
            mc.move(z, z=True, absolute=True)
            self._base = mc.polyBoolOp(self._base[0], panel[0], op=1, n="baseTrainSP#")
            mc.delete(self._base[0], constructionHistory=True)

        # Center circle
        circles = mc.polyCylinder(h=self._width + 2, name="circle#")
        mc.rotate(90, z=True, absolute=True)
        self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainCC#")
        mc.delete(self._base[0], constructionHistory=True)

        # Side circle
        increment = int(self._depth / 10)
        startZ = int((-self._depth / 2) + 2)
        count = 1
        for z in range(startZ, int(self._depth / 2), increment):
            if not (4 <= count <= 6):
                circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)
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
                circleAndRing = mc.polyBoolOp(circles[0], rings[0], op=1, n="hangers#")
                mc.delete(circleAndRing[0], constructionHistory=True)
                mc.move(-self._height * 1 / 3, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circleAndRing[0], op=1, n="baseTrainHR#")
                # Can't do a delete history here, not sure why
            count += 1

    def buildBaseAndWheels(self):
        wheelLocZ = self._depth/2  # quarter along body
        large = 4
        medium = 2
        mediumLocY = 2 + 0.5 + large + medium + 0.1  # (railHeight*2) + plankHeight + largeRadius + mediumRadius

        # 2 Top Wheels
        for i in range(2):
            ws = WheelSet(radius=large)
            ws.buildWheelsAndAxel()
            ws.move(z=wheelLocZ)
            self._wheelSets.append(ws)
            wheelLocZ -= ws.getSize() * 2.5

        # Union
        topWheels = mc.polyBoolOp(self._wheelSets[0].getName(), self._wheelSets[1].getName(), op=1, name="topWheels#")

        # 2 Bottom Wheels
        wheelLocZ = self._depth/2  # Reset
        for i in range(2):
            ws = WheelSet(radius=medium)
            ws.buildWheelsAndAxel()
            ws.move(y=-mediumLocY, z=wheelLocZ)  # Move under tracks
            self._wheelSets.append(ws)
            wheelLocZ -= large * 2.5

        # Union
        bottomWheels = mc.polyBoolOp(self._wheelSets[2].getName(), self._wheelSets[3].getName(), op=1, name="bottomWheels#")
        fourWheels = mc.polyBoolOp(topWheels[0], bottomWheels[0], op=1, name="4wheels#")

        # Build wires
        exWire = Wire()
        wireLocX = (self._wheelSets[0].getAxelLength()/2) + (exWire.getBendRadius()/2) - 0.5  # (axelLength / 2) + (cordBendRadius / 2) - 0.5 #0.5 so it connects to lower wheel
        wireLocZ = self._depth / 2  # So it can be incremented
        wireList = []
        for x in [-wireLocX, wireLocX]: # LeftSide, RightSide
            wireLocZ = self._depth / 2  # So it can be incremented
            for i in range(2):
                wire = Wire()
                wire.createWire()
                wireLocY = wire.getBendRadius()/2
                wire.move(x, -wireLocY, wireLocZ)
                wireLocZ -= large * 2.5
                if x == wireLocX:  #Right
                    mc.rotate(180, z=True, absolute=True)
                self._wires.append(wire)

            if x == -wireLocX: # Left
                wireList.append(mc.polyBoolOp(self._wires[0].getName(), self._wires[1].getName(), op=1, name="leftWires#"))
                mc.delete(wireList[0][0], constructionHistory=True)
            else: # Right
                wireList.append(mc.polyBoolOp(self._wires[2].getName(), self._wires[3].getName(), op=1, name="rightWires#"))
                mc.delete(wireList[1][0], constructionHistory=True)

        fourWires = mc.polyBoolOp(wireList[0][0], wireList[1][0], op=1, name="4wires#")
        mc.delete(fourWires[0], constructionHistory=True)

        allWheelParts = mc.polyBoolOp(fourWheels[0], fourWires[0], op=1, name="allWheelParts#")
        mc.delete(allWheelParts[0], constructionHistory=True)

        # Build Body
        baseLocY = (self._height/2) + mediumLocY
        self.createBaseCar()
        mc.select(self._base, r=True)
        mc.move(-baseLocY, self._width/2, yz=True, absolute=True)  # Line up with wheels

        # Union
        car = mc.polyBoolOp(self._base[0], allWheelParts[0], name="Train#")
        self._names.append(car)
        self.clearHistory()
        # Move up onto tracks, Rail height = 1
        mc.move(large + 1, y=True, absolute=True)  # pivot is created in the center of the top wheel axel

    def getDepth(self):
        return self._depth
