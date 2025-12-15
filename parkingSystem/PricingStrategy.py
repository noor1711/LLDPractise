from abc import ABC, abstractmethod
from datetime import datetime

from Ticket import Ticket


class PricingStrategy(ABC):
    """
    Strategy interface for calculating parking fees.
    """

    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        """
        Calculate the fee for the given ticket.
        """
        raise NotImplementedError


class FlatRatePerHourPricingStrategy(PricingStrategy):
    """
    Simple pricing strategy: flat rate per started hour.
    """

    def __init__(self, rate_per_hour: float) -> None:
        self._rate_per_hour = rate_per_hour

    def calculate_fee(self, ticket: Ticket) -> float:
        if ticket.exitTime is None or ticket.entryTime is None:
            # If for some reason exitTime was not set, treat fee as zero
            return 0.0

        delta = ticket.exitTime - ticket.entryTime
        total_seconds = delta.total_seconds()
        hours = total_seconds / 3600.0

        # Charge for every started hour
        started_hours = int(hours) if hours.is_integer() else int(hours) + 1
        if started_hours == 0:
            started_hours = 1

        return started_hours * self._rate_per_hour


