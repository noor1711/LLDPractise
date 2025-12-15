from abc import ABC, abstractmethod
import Vehicle
import ParkingSpot
from ParkingService import ParkingService
from Ticket import Ticket
from datetime import datetime
from time import sleep
class ParkingLot(ABC):

    def __init__(self):
        self.parkingSvc : ParkingService = ParkingService(1, 5, 10)
        self.tickets = {}
        self.plateToTicketMapping = {}

    def parkCar(self, vehicle:Vehicle.Vehicle):
        if self.parkingSvc.canPark(vehicle):
            spot = self.parkingSvc.parkVechicle(vehicle)
            ticket = Ticket(vehicle=vehicle, spot=spot, entryTime=datetime.now())
            self.tickets[ticket.id] = ticket
            return ticket
        else:
            return None

    def unparkCar(self, ticket: Ticket):
        if ticket.id in self.tickets:
            ticket = self.tickets[ticket.id]
            vehicle = ticket.vehicle
            self.parkingSvc.unparkVehicle(vehicle=vehicle)
            fee = str(ticket.entryTime) 

            return fee
        else:
            return None
        
pl = ParkingLot()
car1 = Vehicle.Car(1)
car2 = Vehicle.Car(2)

truck1 = Vehicle.Truck(10)
truck2 = Vehicle.Truck(11)

t1 = pl.parkCar(car1)
t2 = pl.parkCar(car2)
t3 = pl.parkCar(truck1)
t4 = pl.parkCar(truck2)

sleep(5)

print(pl.unparkCar(t1))
print(pl.unparkCar(t2))
print(pl.unparkCar(t3))
print(t4)