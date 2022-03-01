"""
Mia Seppi
CSANM 258 - Winter 2022

3D Train Set 1.0 - (7th version of all pythonTrainTrackSet)

1.0 version of module set up

"""
import importlib
import sys
sys.path.append("/Users/miaseppi/Code-local/3DTrainSet-1.0/src")

""" Execute code """

import GuiWindowObject
importlib.reload(GuiWindowObject)

print("Track")
myWindow = GuiWindowObject.GuiWindow()


"""For Modeling Purposes"""
import maya.cmds as mc
import TrainObject
import EngineObject
import CarTypeAObject
import CarTypeA2Object
import CarTypeBObject
import CarTypeB2Object
import CarTypeB3Object
import CarTypeCObject
import CarTypeC2Object
importlib.reload(TrainObject)
importlib.reload(EngineObject)
importlib.reload(CarTypeAObject)
importlib.reload(CarTypeA2Object)
importlib.reload(CarTypeBObject)
importlib.reload(CarTypeB2Object)
importlib.reload(CarTypeB3Object)
importlib.reload(CarTypeCObject)
importlib.reload(CarTypeC2Object)


def buildTrainExample():
    cars = [EngineObject.Engine()]
    cars[0].buildBaseAndWheels()

    z = 25
    for carType in range(1, 8):

        if carType == 1:
            cars.append(TrainObject.Train())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 2:
            cars.append(CarTypeAObject.CarTypeA())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 3:
            cars.append(CarTypeBObject.CarTypeB())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 4:
            cars.append(CarTypeB2Object.CarTypeB2())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 5:
            cars.append(CarTypeB3Object.CarTypeB3())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 6:
            cars.append(CarTypeCObject.CarTypeC())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        elif carType == 7:
            cars.append(CarTypeC2Object.CarTypeC2())
            cars[-1].buildBaseAndWheels()
            mc.move(z, z=True, absolute=True)

        z += 25  # Length of a whole train is 29

    cars.append(EngineObject.Engine())
    cars[-1].buildBaseAndWheels()
    d = cars[1].getDepth()
    mc.rotate(180, y=True, absolute=True)
    mc.move(z + d / 2, z=True, absolute=True)  # 29 is the length of a car that allows some overlap for connection

#buildTrainExample()

#car = CarTypeAObject.CarTypeA()
#car.buildBaseAndWheels()

print("\n" + "Program Complete" + "\n")  # Debug Checker
