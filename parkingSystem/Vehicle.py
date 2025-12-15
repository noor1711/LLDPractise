from abc import ABC, abstractmethod
import random
from enum import Enum

class VEHICLE_SIZE(Enum):
    SMALL=1    
    MEDIUM=2
    LARGE=3

class Vehicle(ABC):

    @property
    def size(self) -> VEHICLE_SIZE:
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def numberPlate(self):
        return self._numberPlate

    @numberPlate.setter
    def numberPlate(self, plate):
        self._numberPlate = plate

def getNumberPlate():
    return random.randint(0, 10000)

class Scooter(Vehicle):
    
    def __init__(self, numberPlate):
        self.size = VEHICLE_SIZE.SMALL
        self.numberPlate = numberPlate
    
class Car(Vehicle):

    def __init__(self, numberPlate):
        self.size = VEHICLE_SIZE.MEDIUM
        self.numberPlate = numberPlate

class Truck(Vehicle):

    def __init__(self, numberPlate):
        self.size = VEHICLE_SIZE.LARGE
        self.numberPlate = numberPlate
