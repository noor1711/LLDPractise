from enum import Enum
from typing import List
from uuid import UUID

from Concert import Seat


class BOOKING_STATUS(Enum):
    CANCELLED = 1
    BOOKED = 2
    PENDING = 3


class Booking:
    """
    Represents a booking for specific seats in a concert by a user.
    """

    def __init__(self, bookingId: UUID, userId: UUID, seats: List[Seat], concertId: UUID, amount: float):
        self._bookingId = bookingId
        self._userId = userId
        self._status = BOOKING_STATUS.PENDING
        self._concertId = concertId
        self._seats = seats
        self._amount = amount

    @property
    def bookingId(self) -> UUID:
        return self._bookingId

    @property
    def userId(self) -> UUID:
        return self._userId

    @property
    def status(self) -> BOOKING_STATUS:
        return self._status

    @property
    def seats(self) -> List[Seat]:
        return self._seats

    @property
    def concertId(self) -> UUID:
        return self._concertId

    @property
    def amount(self) -> float:
        return self._amount

    def cancel_booking(self) -> None:
        self._status = BOOKING_STATUS.CANCELLED

    def confirm_booking(self) -> None:
        self._status = BOOKING_STATUS.BOOKED

