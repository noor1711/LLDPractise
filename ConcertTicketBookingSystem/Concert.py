from typing import List, Tuple
from datetime import date
from User import User
from uuid import uuid4
from threading import Lock

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
        self._waitlist: List[Tuple[User, int]] = []
        self._lock = Lock()

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
        """
        View helper: returns up to num_seats currently available seats (without reserving them).
        """
        with self._lock:
            if len(self._available) < num_seats:
                return None
            return list(self._available[:num_seats])

    def reserveSeats(self, seats: List[Seat]) -> bool:
        """
        Atomically reserve the given seats if all are available.
        Returns True on success, False if any seat is already taken.
        """
        with self._lock:
            # ensure all seats are currently available
            for seat in seats:
                if seat not in self._available:
                    return False

            for seat in seats:
                self._available.remove(seat)
            self._booked += len(seats)
            return True

    def unoccupySeats(self, seats: List[Seat]) -> List[Tuple[User, List[Seat]]]:
        """
        Free the given seats and try to satisfy waitlisted requests in FIFO order.
        Returns a list of (user, newly_allocated_seats) for users promoted from the waitlist.
        """
        promoted: List[Tuple[User, List[Seat]]] = []
        with self._lock:
            for seat in seats:
                if seat not in self._available:
                    self._available.append(seat)
                    self._booked -= 1

            # Process waitlist in FIFO manner
            while self._waitlist and len(self._available) >= self._waitlist[0][1]:
                user, num_required = self._waitlist.pop(0)
                allocated = self._available[:num_required]
                for seat in allocated:
                    self._available.remove(seat)
                self._booked += num_required
                promoted.append((user, allocated))

        return promoted

    def add_to_waitlist(self, user: User, num_seats: int):
        with self._lock:
            self._waitlist.append((user, num_seats))
    