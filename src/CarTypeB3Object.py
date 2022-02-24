import maya.cmds as mc
from TrainObject import Train

# Mix of Default and TypeB
# Default Lower and TypeB Upper


class CarTypeB3(Train):
    def _createUpperCar(self):
        octagon = 8

        self._base = mc.polyCube(w=self._width, h=self._height, d=self._depth, name="bodyBase#")
        mc.polyBevel(self._base[0], offset=self._carBevel)

        self._connectors()

        # Side circles
        startY = 0
        for y in range(startY, int(-self._height * 1/3), -2):
            increment = int(self._depth / 10)
            startZ = int((-self._depth / 2) + 2)
            for z in range(startZ, int(self._depth / 2), increment):
                circles = mc.polyCylinder(r=0.5, h=self._width + 0.25, subdivisionsAxis=octagon, name="circle#")
                mc.rotate(90, z=True, absolute=True)
                mc.move(y, z, yz=True, absolute=True)  # Shift down
                self._base = mc.polyBoolOp(self._base[0], circles[0], op=1, n="baseTrainC#")
                mc.delete(self._base[0], constructionHistory=True)

        # Hangers of the lower compartment
        self._hangers()

        lowerBox = self._createLowerCar()
        self._base = mc.polyBoolOp(self._base[0], lowerBox[0], op=1, n="body#")
