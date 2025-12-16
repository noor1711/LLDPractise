from threading import Lock
from datetime import datetime, timedelta
from typing import List
from User import User
from Bid import Bid
from uuid import uuid4, UUID

class Listing:

    def __init__(self, initial_price: int, duration: timedelta, name: str, description: str, listed_by: User):
        self._id: UUID = uuid4()
        self._price = initial_price
        self._end_time = datetime.now() + duration
        self._name = name
        self._description = description
        self._listed_by = listed_by
        self._current_bid = None
        self._subscribers: List[User] = []
        self._lock = Lock()

    @property
    def listing_id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description

    @property
    def listed_by(self):
        return self._listed_by
    
    def is_listing_valid(self):
        return datetime.now() < self._end_time

    
    def add_new_bid(self, bid: Bid) -> bool:
        
        # I think subscribers should be a seperate entity of its own but fine
        if bid.bidder not in self._subscribers:
            self._subscribers.append(bid.bidder)

        if self.is_listing_valid() and bid.price > self._price:
            with self._lock:
                if self.is_listing_valid() and bid.price > self._price:
                    self._current_bid = bid
                    self._price = bid.price
                    message = "Bid for", self._name, " is currently at", self._current_bid.price
                    self.notify_subscribers(message)
                    bid.accept_bid()
                    return True
                
        bid.reject_bid()
        return False

    def notify_subscribers(self, message):
        for subscriber in self._subscribers:
            subscriber.update(message)

    def handle_bidding_close(self):
        message = "Bid for", self._name, " is closed, winner is ", self._current_bid.bidder.name
        self.notify_subscribers(message)
    
