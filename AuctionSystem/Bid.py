from User import User
from enum import Enum

class BIDDING_STATE(Enum):
    ACCEPTED=1
    REJECTED=2
    PENDING=3

class Bid:

    def __init__(self, price: int, bidder: User):
        self._price: int = price
        self._bidder: User = bidder
        self._state: BIDDING_STATE = BIDDING_STATE.PENDING

    @property
    def state(self) -> BIDDING_STATE:
        return self._state

    @property
    def price(self):
        return self._price

    @property
    def bidder(self) -> User:
        return self._bidder
        
    def accept_bid(self):
        self._state = BIDDING_STATE.ACCEPTED

    def reject_bid(self):
        self._state = BIDDING_STATE.REJECTED