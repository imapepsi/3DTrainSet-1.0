import maya.cmds as mc
from MayaObject import MayaObj
import TrackObject
import TrainObject
import EngineObject
import CarTypeAObject
import CarTypeBObject
import CarTypeCObject
import CarTypeDObject
import CarTypeEObject
from random import seed
from random import randint
from time import time

import importlib
importlib.reload(TrackObject)
importlib.reload(TrainObject)
importlib.reload(EngineObject)
importlib.reload(CarTypeAObject)
importlib.reload(CarTypeBObject)
importlib.reload(CarTypeCObject)
importlib.reload(CarTypeDObject)
importlib.reload(CarTypeEObject)


class TrainTrackSet(MayaObj):
    def __init__(self, numPlanks=5, numTracks=1, numCars=3):
        self._numPlanks = numPlanks
        self._numTracks = numTracks
        self._numCars = numCars
        self._tracks = []  # List of Track obj
        self._engine = []
        self._cars = []

    def buildTracks(self):
        """Build user input number of tracks"""

        trackLocZ = 0
        for i in range(self._numTracks):  # So I don't have to calculate where to stop
            t = TrackObject.TrainTrackObj(numPlanks=self._numPlanks)
            t.buildPlanks()
            t.buildRails()
            t.addBolts()
            t.unionAll()
            t.move(z=trackLocZ)
            trackLocZ += t.getTrackDepth()
            self._tracks.append(t)

    def getTrackList(self):
        return self._tracks

    def setNumTracks(self, numTracks):
        self._numTracks = numTracks

    def setNumCars(self, numCars):
        self._numCars = numCars

    def buildTrain(self):
        self._engine.append(EngineObject.Engine())
        self._engine[0].buildBaseAndWheels()

        seed(time())
        z = 25
        for i in range(self._numCars):
            carType = randint(1, 6)

            if carType == 1:
                self._cars.append(TrainObject.Train())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 2:
                self._cars.append(CarTypeAObject.CarTypeA())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 3:
                self._cars.append(CarTypeBObject.CarTypeB())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 4:
                self._cars.append(CarTypeCObject.CarTypeC())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 5:
                self._cars.append(CarTypeDObject.CarTypeD())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 6:
                self._cars.append(CarTypeEObject.CarTypeE())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            z += 25  # Length of a whole train is 29

        self._engine.append(EngineObject.Engine())
        self._engine[1].buildBaseAndWheels()
        d = self._engine[1].getDepth()
        mc.rotate(180, y=True, absolute=True)
        mc.move(z + d/2, z=True, absolute=True)  # 29 is the length of a car that allows some overlap for connection
