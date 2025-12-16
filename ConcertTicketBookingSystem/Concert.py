from typing import List
from datetime import date
from User import User
from uuid import uuid4

class Seat:
    def __init__(self, seat_id: int):
        self._id = seat_id
        self._is_available = True

    @property
    def seatId(self):
        return self._id

    def isAvailable(self):
        return self._is_available

    def occupy(self):
        self._is_available = False

class Concert:

    def __init__(self, venue: str, artist: str, date: date, num_seats: int):
        self._concertId = uuid4()
        self._venue = venue
        self._artist = artist
        self._date = date
        self._total_seats = num_seats
        self.seats: List[Seat] = [Seat(i) for i in range(num_seats)]
        self._available: List[Seat] = self.seats
        self._booked = 0
        self._waitlist = []

    @property
    def concertId(self):
        return self._concertId

    @property
    def artist(self):
        return self._artist

    @property
    def venue(self):
        return self._venue
    
    @property
    def date(self):
        return self._date
    
    def getSeats(self, num_seats: int):
        if len(self._available) < num_seats:
            return None

        return self._available[:num_seats]

    def occupySeats(self, seats: List[Seat]) -> bool:
        
        self._booked += len(seats)
        [self._available.remove(seat) for seat in seats if seat in self._available]

    def unoccupySeats(self, seats: List[Seat]) -> bool:
        
        self._booked -= len(seats)
        [self._available.append(seat) for seat in seats]

    def add_to_waitlist(self, user: User, num_seats: int):
        self._waitlist.append([user, num_seats])
    