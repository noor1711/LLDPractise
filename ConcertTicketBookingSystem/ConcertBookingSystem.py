from uuid import UUID, uuid4
from typing import Dict, List
from datetime import date

from Concert import Concert, Seat
from User import User
from Booking import Booking
from SearchStrategy import (
    SearchStrategy,
    VenueBasedSearchStrategy,
    ArtistBasedSearchStrategy,
    DateBasedSearchStrategy,
)
from PaymentService import PaymentService, DummyPaymentService
from NotificationService import NotificationService, ConsoleNotificationService


class ConcertBookingSystem:

    def __init__(
        self,
        payment_service: PaymentService | None = None,
        notification_service: NotificationService | None = None,
    ):
        self._concerts: Dict[UUID, Concert] = {}
        self._users: Dict[UUID, User] = {}
        self._bookings: Dict[UUID, Booking] = {}
        self._payment_service: PaymentService = payment_service or DummyPaymentService()
        self._notification_service: NotificationService = (
            notification_service or ConsoleNotificationService()
        )
    
    def addConcert(self, venue: str, artist: str, concert_date: date, num_seats: int = 1000) -> UUID:
        """
        Create a concert. In a real system, seat count would come from the venue.
        """
        concert = Concert(venue, artist, concert_date, num_seats)
        self._concerts[concert.concertId] = concert
        return concert.concertId

    def addUser(self, name: str) -> UUID:
        user = User(name)
        self._users[user.userId] = user
        return user.userId

    def getSeatsForConcert(self, concertId: UUID, num_seats: int) -> List[Seat] | None:
        concert: Concert | None = self._concerts.get(concertId)
        if concert is None:
            return None

        return concert.getSeats(num_seats)

    def bookSeatsForConcert(self, userId: UUID, concertId: UUID, seats: List[Seat]) -> UUID | None:
        """
        Reserve seats atomically, process payment, and confirm booking.
        Booking remains PENDING until payment succeeds.
        """
        user: User | None = self._users.get(userId)
        concert: Concert | None = self._concerts.get(concertId)
        if user is None or concert is None:
            return None

        # Atomically reserve seats to avoid double-booking
        if not concert.reserveSeats(seats):
            return None

        amount = float(len(seats)) * 100.0  # simple flat pricing per seat
        bookingId = uuid4()
        booking = Booking(bookingId, userId, seats, concertId, amount)
        self._bookings[bookingId] = booking

        # Process payment
        if not self._payment_service.process_payment(user, amount):
            # Payment failed, release seats and cancel booking
            concert.unoccupySeats(seats)
            booking.cancel_booking()
            return None

        # Payment succeeded; confirm booking and notify user
        booking.confirm_booking()
        self._notification_service.send_booking_confirmation(user, booking)
        return bookingId
    
    def cancelBooking(self, bookingId: UUID, userId: UUID) -> bool:
        """
        Cancel a booking if it exists and is owned by the given user.
        Freed seats are offered to the waitlist in FIFO order.
        """
        booking: Booking | None = self._bookings.get(bookingId)
        if not booking:
            return False

        if booking.userId != userId:
            # Enforce ownership
            return False
        
        booking.cancel_booking()
        seats = booking.seats
        concertId = booking.concertId

        concert: Concert | None = self._concerts.get(concertId)
        if concert is None:
            return False

        promoted = concert.unoccupySeats(seats)

        # Create new bookings for promoted waitlist users
        for promoted_user, allocated_seats in promoted:
            amount = float(len(allocated_seats)) * 100.0
            promoted_booking_id = uuid4()
            promoted_booking = Booking(
                promoted_booking_id,
                promoted.userId,
                allocated_seats,
                concertId,
                amount,
            )
            self._bookings[promoted_booking_id] = promoted_booking

            # For simplicity, assume payment succeeds for waitlist promotions
            promoted_booking.confirm_booking()
            self._notification_service.send_waitlist_promotion(promoted_user, promoted_booking)

        return True

    def waitlistForConcert(self, userId: UUID, concertId: UUID, numSeats: int) -> str:
        concert: Concert | None = self._concerts.get(concertId)

        if concert is None:
            return "Invalid Concert"

        user: User | None = self._users.get(userId)

        if user is None:
            return "Invalid User"
        
        concert.add_to_waitlist(user, numSeats)
        return "WaitListed"
    
    def search(self, searchStrategy: SearchStrategy, keyword):
        return searchStrategy.search(list(self._concerts.values()), keyword)


if __name__ == "__main__":
    system = ConcertBookingSystem()
    
    c1 = system.addConcert("Delhi", "AP dhillon", date.fromisocalendar(2025, 43, 1))
    u1 = system.addUser("Noor")
    u2 = system.addUser("Nimrat")

    seats = system.getSeatsForConcert(c1, 10)
    print(len(seats))
    b1 = system.bookSeatsForConcert(u1, c1, seats)
    print(b1)

    # Add some more concerts and search
    system.addConcert("Delhi", "Karan Aujla", date.fromisocalendar(2025, 43, 1))
    system.addConcert("Mumbai", "Coldplay", date.fromisocalendar(2025, 43, 1))
    concerts = system.search(VenueBasedSearchStrategy(), "Delhi")
    print(len(concerts))
    print(len(system.search(DateBasedSearchStrategy(), date.fromisocalendar(2025, 43, 1))))
