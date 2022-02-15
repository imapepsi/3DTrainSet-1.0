"""
Mia Seppi
CSANM 258 - Winter 2022

3D Train Set 1.0 - (6th version of pythonTrainTrackSet)

"""

import sys
sys.path.append("/Users/miaseppi/Code-local/3DTrainSet-1.0/src")

from GuiWindowObject import GuiWindow
import TrackObject

""" Execute code """


def buildTrack():
    t = TrackObject.TrainTrackObj()
    t.buildPlanks()
    t.buildRails()
    t.addBolts()

print("Track")
myWindow = GuiWindow()

#buildTrack()

print("\n" + "Program Complete" + "\n")  # Debug Checker
