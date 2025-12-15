from abc import ABC
from random import randint
class Ticket(ABC):

    def __init__(self, vehicle, spot, entryTime):
        self._vehicle = vehicle
        self._spot = spot
        self.entryTime = entryTime
        self.id = randint(0, 10000000)

    @property
    def vehicle(self):
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle):
        self._vehicle = vehicle
    
    @property
    def spot(self):
        return self._spot

    @spot.setter
    def spot(self, spot):
        self._spot = spot
    
    @property
    def entryTime(self):
        return self._entryTime
    
    @entryTime.setter
    def entryTime(self, time):
        self._entryTime = time
    
    @property
    def exitTime(self):
        return self._exitTime
    
    @entryTime.setter
    def exitTime(self, time):
        self._exitTime = time
    
    