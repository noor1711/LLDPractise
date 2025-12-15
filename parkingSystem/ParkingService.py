from abc import ABC, abstractmethod
import Vehicle
import ParkingSpot

class ParkingService(ABC):
    def __init__(self, largeSpots, mediumSpots, smallSpots):
        self.available = {}

        large = [ParkingSpot.LargeSpot()] * largeSpots
        medium = [ParkingSpot.MediumSpot()] * mediumSpots
        small = [ParkingSpot.SmallSpot()] * smallSpots
        self.available[Vehicle.VEHICLE_SIZE.SMALL] = small
        self.available[Vehicle.VEHICLE_SIZE.MEDIUM] = medium
        self.available[Vehicle.VEHICLE_SIZE.LARGE] = large
        
        self.occupied = {}

    def canPark(self, vehicle: Vehicle.Vehicle):
        if len(self.available[vehicle.size]):
            return True
        return False

    def parkVechicle(self, vehicle):
        spot = self.available[vehicle.size].pop()
        spot.parkVehicle(vehicle)
        self.occupied[vehicle.numberPlate] = spot
        print(self.available, self.occupied)
        return spot
    
    def unparkVehicle(self, vehicle):
        if vehicle.numberPlate in self.occupied:
            spot = self.occupied[vehicle.numberPlate]
            spot.unparkVehicle()
            del self.occupied[vehicle.numberPlate]
            self.available[vehicle.size].append(spot)
            print(self.available, self.occupied)
            return spot
        else:
            return None
        
# svc = ParkingService(10, 0, 1)
# v = Vehicle.Car(1)
# p = Vehicle.Car(2)
# print(svc.canPark(v))
# print(svc.parkVechicle(v))
# print(svc.canPark(p))