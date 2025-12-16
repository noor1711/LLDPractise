from abc import ABC, abstractmethod

from User import User


class PaymentService(ABC):
    """
    Abstraction for processing payments.
    """

    @abstractmethod
    def process_payment(self, user: User, amount: float) -> bool:
        """
        Returns True if payment succeeds, False otherwise.
        """
        raise NotImplementedError


class DummyPaymentService(PaymentService):
    """
    Simple implementation that always succeeds.
    In a real system, this would integrate with a payment gateway.
    """

    def process_payment(self, user: User, amount: float) -> bool:
        # For now, always succeed. Logging could be added here.
        return True


