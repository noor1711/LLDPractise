from typing import Dict, List

import Vehicle
import ParkingSpot


class ParkingService:
    """
    Service responsible for allocating and freeing parking spots.
    Keeps track of available and occupied spots by vehicle size.
    """

    def __init__(self, largeSpots: int, mediumSpots: int, smallSpots: int) -> None:
        # size -> list of available spots
        self.available: Dict[Vehicle.VEHICLE_SIZE, List[ParkingSpot.ParkingSpot]] = {}

        # Create distinct spot instances
        large = [ParkingSpot.LargeSpot() for _ in range(largeSpots)]
        medium = [ParkingSpot.MediumSpot() for _ in range(mediumSpots)]
        small = [ParkingSpot.SmallSpot() for _ in range(smallSpots)]

        self.available[Vehicle.VEHICLE_SIZE.SMALL] = small
        self.available[Vehicle.VEHICLE_SIZE.MEDIUM] = medium
        self.available[Vehicle.VEHICLE_SIZE.LARGE] = large

        # number_plate -> occupied spot
        self.occupied: Dict[int, ParkingSpot.ParkingSpot] = {}

    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        """
        Returns True if there is at least one available spot for the vehicle.
        """
        return len(self.available.get(vehicle.size, [])) > 0

    def park_vehicle(self, vehicle: Vehicle.Vehicle) -> ParkingSpot.ParkingSpot:
        """
        Parks the vehicle and returns the allocated spot.
        Raises an exception if no spot is available.
        """
        spots_for_size = self.available.get(vehicle.size, [])
        if not spots_for_size:
            raise RuntimeError("No available spots for vehicle size")

        spot = spots_for_size.pop()
        spot.parkVehicle(vehicle)
        self.occupied[vehicle.numberPlate] = spot
        return spot

    def unpark_vehicle(self, vehicle: Vehicle.Vehicle) -> ParkingSpot.ParkingSpot | None:
        """
        Unparks the given vehicle, making its spot available again.
        Returns the freed spot, or None if the vehicle was not parked.
        """
        spot = self.occupied.get(vehicle.numberPlate)
        if spot is None:
            return None

        spot.unparkVehicle()
        del self.occupied[vehicle.numberPlate]
        self.available[vehicle.size].append(spot)
        return spot
        
# svc = ParkingService(10, 0, 1)
# v = Vehicle.Car(1)
# p = Vehicle.Car(2)
# print(svc.canPark(v))
# print(svc.parkVechicle(v))
# print(svc.canPark(p))