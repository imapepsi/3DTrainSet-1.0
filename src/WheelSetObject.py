import maya.cmds as mc
from MayaObject import MayaObj


class WheelSet(MayaObj):
    def __init__(self, radius=1.0, guardH=0.3, bodyBaseWidth=10):
        self._names = []  # Name of wheel set
        self._wheels = []
        self._axel = []
        self._coreH = 1.0 + 0.3 + 0.01  # railGuardTopWidth + 0.3 for guard 0.01 is for gap between guard and rail
        self._coreR = radius
        self._guardH = guardH
        self._guardR = radius + 0.2  # 0.2 > core radius
        self._capR = radius*3/4
        self._axelR = radius/4
        self._axelH = bodyBaseWidth + guardH*2 + (1.0 + 0.3 + 0.01)  # bodyBaseWidth + (guardHeight * 2) + coreHeight

    def createWheel(self):
        """Create 1 wheel"""
        capScale = 0.25

        core = mc.polyCylinder(h=self._coreH, r=self._coreR, n="wheelCore#")

        guard = mc.polyCylinder(h=self._guardH, r=self._guardR, n="wheelGaurd#")
        mc.move(self._coreH/2, y=True, absolute=True)

        cap = mc.polySphere(r=self._capR, n="cap#")
        mc.scale(capScale, scaleY=True, absolute=True)
        mc.move((-self._coreH/2), y=True, absolute=True)

        mainWheelParts = mc.polyBoolOp(core[0], guard[0], op=1, n='coreAndGuard#')
        wheel = mc.polyBoolOp(mainWheelParts[0], cap[0], op=1, n="wheel#")
        mc.delete(wheel[0], constructionHistory=True)
        self._wheels.append(wheel)

    def createAxel(self):
        self._axel = mc.polyCylinder(h=self._axelH, r=self._axelR, n="axel#")

    def buildWheelsAndAxel(self):
        endOfAxel = self._axelH/2  # /2 because wheel starts at 0,0 in the middle of the axel

        # axel
        self.createAxel()
        axel = self._axel[0]

        # left -
        mc.select(d=True)
        self.createWheel()
        left = self._wheels[0][0]
        mc.select(left, replace=True)
        mc.move(-endOfAxel, y=True, absolute=True)

        # right
        mc.select(d=True)
        self.createWheel()
        right = self._wheels[1][0]
        mc.select(right, replace=True)
        mc.rotate(180, z=True, absolute=True)  # 180 - Flip wheel over
        mc.move(endOfAxel, y=True, absolute=True)

        # Union
        wPair = mc.polyBoolOp(right, left, n="wheelPair#")
        self._names = mc.polyBoolOp(axel, wPair[0], n="axelWheelSet#")
        mc.rotate(90, z=True, absolute=True)  # Vertical to horizontal position
        self.clearHistory()

    def getSize(self):
        return self._coreR

    def getAxelLength(self):
        return self._axelH
