from abc import ABC, abstractmethod

from User import User
from Booking import Booking


class NotificationService(ABC):
    """
    Abstraction for sending notifications (email/SMS/etc.).
    """

    @abstractmethod
    def send_booking_confirmation(self, user: User, booking: Booking) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_waitlist_promotion(self, user: User, booking: Booking) -> None:
        raise NotImplementedError


class ConsoleNotificationService(NotificationService):
    """
    Simple implementation that prints notifications to the console.
    In a real system, this would send emails/SMS.
    """

    def send_booking_confirmation(self, user: User, booking: Booking) -> None:
        print(f"Booking confirmed for user {user.userId}: booking {booking.bookingId}, amount {booking.amount}")

    def send_waitlist_promotion(self, user: User, booking: Booking) -> None:
        print(f"Waitlist promoted for user {user.userId}: booking {booking.bookingId}, amount {booking.amount}")


