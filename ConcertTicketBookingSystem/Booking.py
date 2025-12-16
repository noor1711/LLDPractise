from enum import Enum

class BOOKING_STATUS(Enum):
    CANCELLED=1
    BOOKED=2
    PENDING=3

class Booking:

    def __init__(self, bookingId, seats, concertId):
        self._bookingId = bookingId
        self._status = BOOKING_STATUS.PENDING
        self._concertId = concertId
        self._seats = seats
    
    @property
    def bookingId(self):
        return self._bookingId

    @property
    def status(self):
        return self._status

    def cancel_booking(self):
        self._status = BOOKING_STATUS.CANCELLED
    
    def confirm_booking(self):
        self._status = BOOKING_STATUS.BOOKED
    
