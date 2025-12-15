from abc import ABC, abstractmethod
from enum import Enum
import Vehicle

class PARKING_SPOT_SIZE(Enum):
    SMALL=1    
    MEDIUM=2
    LARGE=3


class ParkingSpot(ABC):

    def __init__(self):
        super().__init__()
        self._isAvailable = True
        self._vehicle: Vehicle.Vehicle | None = None

    @property
    def size(self) -> PARKING_SPOT_SIZE:
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def isAvailable(self) -> bool:
        return self._isAvailable
    
    @isAvailable.setter
    def isAvailable(self, value: bool):
        self._isAvailable = value
    
    @property
    def vehicle(self) -> Vehicle.Vehicle | None:
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle):
        self._vehicle = vehicle
    
    def parkVehicle(self, vehicle):
        if self.isAvailable:
            self.isAvailable = False
            self.vehicle = vehicle

    def unparkVehicle(self):
        self._isAvailable = True
        self.vehicle = None

class SmallSpot(ParkingSpot):

    def __init__(self):
        super().__init__()
        self.size = PARKING_SPOT_SIZE.SMALL


class MediumSpot(ParkingSpot):

    def __init__(self):
        super().__init__()
        self.size = PARKING_SPOT_SIZE.MEDIUM
    

class LargeSpot(ParkingSpot):

    def __init__(self):
        super().__init__()
        self.size = PARKING_SPOT_SIZE.LARGE