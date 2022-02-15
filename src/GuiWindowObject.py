import maya.cmds as mc
import TrainTrackSetObject

import importlib
importlib.reload(TrainTrackSetObject)


class GuiWindow:
    def __init__(self):
        """Constructor for Track Builder"""
        self.window = "Train_Set"
        self.title = "Track Builder"  # Display title
        self.size = (400, 400)
        self._numTracks = 0
        self._numCars = 0
        self._buildTrackButton = 0

        # close an old window if open
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)

        # create new window
        self.window = mc.window(self.window, title=self.title, widthHeight=self.size)

        # Layout
        mc.columnLayout(adjustableColumn=True)

        # Ui Features
        mc.separator(height=20)
        self._numTracks = mc.intSliderGrp(field=True, label='Number of Tracks', minValue=1, maxValue=3, fieldMinValue=1, fieldMaxValue=3, value=0)
        mc.separator(height=20)
        self._numCars = mc.intSliderGrp(field=True, label='Number of Cars', minValue=3, maxValue=6, fieldMinValue=3, fieldMaxValue=6, value=0)
        self._buildTrackButton = mc.button(label='Build Train', command=self.buildUserTrainSet)

        # display new window
        mc.showWindow()

    def buildUserTrainSet(self, *args):
        print("Building Train Set...")

        mc.select(clear=True)  # Clear out any data
        mc.select(all=True)
        mc.delete()

        trackSet = TrainTrackSetObject.TrainTrackSet()
        numTracks = mc.intSliderGrp(self._numTracks, query=True, value=True)  # Get number from UI
        trackSet.setNumTracks(numTracks)
        trackSet.buildTracks()

        numCars = mc.intSliderGrp(self._numCars, query=True, value=True)  # Get number from UI
        trackSet.setNumCars(numCars)
        trackSet.buildTrain()

        lambert = mc.shadingNode('lambert', asShader=True)
        mc.select(all=True)
        mc.hyperShade(assign=lambert)
