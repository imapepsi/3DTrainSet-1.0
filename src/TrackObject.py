import maya.cmds as mc
from MayaObject import MayaObj
from PlankObject import Plank
from RailObject import Rail
from BoltSetObject import BoltSet


class TrainTrackObj(MayaObj):
    def __init__(self, numPlanks=5, plankSpacing=4):
        self._names = []
        self._planks = []  # List of class later changes to num of union obj
        self._rails = []  # List of class later changes to num of union obj
        self._boltSets = []  # List of class later changes to num of union obj
        self._trackDepth = 0.0
        self._numPlanks = numPlanks
        self._plankSpacing = plankSpacing
        self._railPlankEdgeOffset = 1.0
        self._railLocX = 0.0

    def buildPlanks(self):
        """Build planks from chosen number of planks"""
        startZ = 0
        for z in range(startZ, self._numPlanks*self._plankSpacing, self._plankSpacing):
            plank = Plank()
            plank.createPlank()
            mc.move(-plank.getHeight()/2, z, yz=True, absolute=True)  # move objects to position and level with 0
            self._planks.append(plank)

    def buildRails(self):
        """Build 4 rails"""
        plankWidth = self._planks[0].getWidth()
        plankHeight = self._planks[0].getHeight()
        plankDepth = self._planks[0].getDepth()
        depth = (self._plankSpacing * (self._numPlanks - 1)) + plankDepth  # FencePost Problem
        self._trackDepth = depth  # Depth save for later

        railLocX = (plankWidth/2) - self._railPlankEdgeOffset
        self._railLocX = railLocX  # Save for later
        railLocY = -plankHeight
        railLocZ = (depth/2) - (plankDepth/2)  # Move rail onto all planks (assuming pivot is the center of the rail)

        count = 1
        for x in [railLocX, -railLocX, railLocX, -railLocX]: # TopRight, TopLeft, UnderRight, UnderLeft
            if count > 2:
                underRail = Rail(depth)
                underRail.createRail()
                underRail.flipRail()
                underRail.move(x=x, y=railLocY, z=railLocZ)
                self._rails.append(underRail)
            else:
                topRail = Rail(depth)
                topRail.createRail()
                topRail.move(x=x, z=railLocZ)
                self._rails.append(topRail)
            count = count + 1

    def addBolts(self):
        """Add bolt sets in correct place based on plank and rail position"""
        plankDepth = self._planks[0].getDepth()
        plankHeight = self._planks[0].getHeight()
        railGuardW = self._rails[0].getTopW()

        boltLocXOut = self._railLocX + railGuardW/2 # Bolt will sit under the edge of TOP rail guard
        boltLocXIn = self._railLocX - railGuardW/2

        # Outside Right

        for x in [boltLocXOut, boltLocXIn, -boltLocXIn, -boltLocXOut]: # OutsideRight, InsideRight, InsideLeft, OutsideLeft
            startZ = 0
            for z in range(startZ, self._numPlanks * self._plankSpacing, self._plankSpacing):
                boltS = BoltSet()
                boltS.createSet(plankDepth, plankHeight)
                boltS.move(x=x, z=z)
                self._boltSets.append(boltS)

    def unionAll(self):
        # Select all parts
        mc.select(clear=True)

        pSet = mc.polyBoolOp(self._planks[0].getName(), self._planks[1].getName(), op=1, name="plankSet#")
        for i in range(2, len(self._planks)):
            pSet = mc.polyBoolOp(pSet[0], self._planks[i].getName(), op=1, name="plankSet#")
        self._planks = pSet
        mc.delete(self._planks[0], constructionHistory=True)

        rSet = mc.polyBoolOp(self._rails[0].getName(), self._rails[1].getName(), op=1, name="railSet#")
        for i in range(2, len(self._rails)):
            rSet = mc.polyBoolOp(rSet[0], self._rails[i].getName(), op=1, name="railSet#")
        self._rails = rSet
        mc.delete(self._rails[0], constructionHistory=True)

        bSet = mc.polyBoolOp(self._boltSets[0].getName(), self._boltSets[1].getName(), op=1, name="boltSetU#")
        for i in range(2, len(self._boltSets)):
            bSet = mc.polyBoolOp(bSet[0], self._boltSets[i].getName(), op=1, name="boltSetU#")
        self._boltSets = bSet
        mc.delete(self._boltSets[0], constructionHistory=True)

        mc.select(clear=True)

        self._names = mc.polyBoolOp(self._planks[0], self._rails[0], op=1, name="TrainTrackA#")
        self._names = mc.polyBoolOp(self._names[0], self._boltSets[0], op=1, name="TrainTrack#")
        # Pivot will be center of the first plank
        self.clearHistory()

    def getTrackDepth(self):
        return self._trackDepth
