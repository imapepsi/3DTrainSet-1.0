import maya.cmds as mc


class MayaObj:
    def __init__(self):
        self._names = []

    def getName(self):
        """Get Obj Name"""
        return self._names[0]

    def move(self, x=0.0, y=0.0, z=0.0):
        mc.select(clear=True)
        mc.select(self._names[0], r=True)
        mc.move(x, y, z, absolute=True)

    def clearHistory(self):
        mc.delete(self._names[0], constructionHistory=True)
