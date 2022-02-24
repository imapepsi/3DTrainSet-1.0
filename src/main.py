"""
Mia Seppi
CSANM 258 - Winter 2022

3D Train Set 1.0 - (7th version of all pythonTrainTrackSet)

1.0 version of module set up

"""
import importlib
import sys
sys.path.append("/Users/miaseppi/Code-local/3DTrainSet-1.0/src")

import GuiWindowObject
importlib.reload(GuiWindowObject)

""" Execute code """

print("Track")
myWindow = GuiWindowObject.GuiWindow()

import CarTypeEObject
importlib.reload(CarTypeEObject)

#car = CarTypeEObject.CarTypeE()
#car.buildBaseAndWheels()

print("\n" + "Program Complete" + "\n")  # Debug Checker
