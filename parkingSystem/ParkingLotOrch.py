from datetime import datetime
from typing import Dict, Optional

import Vehicle
from ParkingService import ParkingService
from Ticket import Ticket
from PricingStrategy import PricingStrategy


class ParkingLot:
    """
    Orchestrator for parking operations.
    Coordinates ParkingService and PricingStrategy and manages ticket lifecycle.
    """

    def __init__(
        self,
        parking_service: ParkingService,
        pricing_strategy: PricingStrategy,
    ) -> None:
        self._parking_service: ParkingService = parking_service
        self._pricing_strategy: PricingStrategy = pricing_strategy
        # ticket_id -> Ticket
        self._tickets: Dict[int, Ticket] = {}
        # number_plate -> ticket_id
        self._plate_to_ticket: Dict[int, int] = {}

    def park_vehicle(self, vehicle: Vehicle.Vehicle) -> Optional[Ticket]:
        """
        Attempts to park the given vehicle.
        Returns a Ticket on success, or None if no spot is available.
        """
        if not self._parking_service.can_park(vehicle):
            return None

        spot = self._parking_service.park_vehicle(vehicle)
        ticket = Ticket(vehicle=vehicle, spot=spot, entryTime=datetime.now())

        self._tickets[ticket.id] = ticket
        self._plate_to_ticket[vehicle.numberPlate] = ticket.id
        return ticket

    def unpark_vehicle(self, ticket: Ticket) -> Optional[float]:
        """
        Unparks the vehicle corresponding to the given ticket.
        Returns the parking fee, or None if the ticket is invalid.
        """
        stored_ticket = self._tickets.get(ticket.id)
        if stored_ticket is None:
            return None

        vehicle = stored_ticket.vehicle
        # Update ticket exit time
        stored_ticket.exitTime = datetime.now()

        # Release the spot
        self._parking_service.unpark_vehicle(vehicle=vehicle)

        # Calculate fee and clean up state
        fee = self._pricing_strategy.calculate_fee(stored_ticket)

        del self._tickets[stored_ticket.id]
        if vehicle.numberPlate in self._plate_to_ticket:
            del self._plate_to_ticket[vehicle.numberPlate]

        return fee


if __name__ == "__main__":
    # Simple demo usage
    from PricingStrategy import FlatRatePerHourPricingStrategy

    parking_service = ParkingService(largeSpots=1, mediumSpots=5, smallSpots=10)
    pricing_strategy = FlatRatePerHourPricingStrategy(rate_per_hour=10.0)

    lot = ParkingLot(parking_service=parking_service, pricing_strategy=pricing_strategy)

    car1 = Vehicle.Car(1)
    car2 = Vehicle.Car(2)
    truck1 = Vehicle.Truck(10)

    t1 = lot.park_vehicle(car1)
    t2 = lot.park_vehicle(car2)
    t3 = lot.park_vehicle(truck1)

    # In a real system we would have time elapse here before unparking
    if t1:
        print("Fee for car1:", lot.unpark_vehicle(t1))
    if t2:
        print("Fee for car2:", lot.unpark_vehicle(t2))
    if t3:
        print("Fee for truck1:", lot.unpark_vehicle(t3))