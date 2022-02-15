import maya.cmds as mc
from MayaObject import MayaObj
from TrackObject import TrainTrackObj
from TrainObject import Train
from EngineObject import Engine
from CarTypeAObject import CarTypeA
from random import seed
from random import randint
from time import time


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
        for i in range(self._numTracks):
            t = TrainTrackObj(numPlanks=self._numPlanks)
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
        self._engine.append(Engine())
        self._engine[0].buildBaseAndWheels()

        seed(time())
        z = 25
        for i in range(self._numCars):
            carType = randint(1, 2)

            if carType == 1:
                self._cars.append(Train())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            elif carType == 2:
                self._cars.append(CarTypeA())
                self._cars[-1].buildBaseAndWheels()
                mc.move(z, z=True, absolute=True)

            z += 25 # Length of a whole train is 29

        self._engine.append(Engine())
        self._engine[1].buildBaseAndWheels()
        d = self._engine[1].getDepth()
        mc.rotate(180, y=True, absolute=True)
        mc.move(z + d/2, z=True, absolute=True)  # 29 is the length of a car that allows some overlap for connection
