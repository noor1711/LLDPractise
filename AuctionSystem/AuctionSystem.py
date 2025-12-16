from User import User
from Bid import Bid
from Listing import Listing
from SearchStrategy import SearchStrategy, NameSearchStrategy

from datetime import timedelta
from typing import Dict, List
from uuid import uuid4, UUID

class AuctionSystem:

    def __init__(self):
        self._users: Dict[UUID, User] = {}
        self._listings: Dict[UUID, Listing] = {}
    
    def get_valid_user(self, user_id: UUID):
        return self._users.get(user_id)

    def get_valid_listing(self, listing_id: UUID):
        return self._listings.get(listing_id)

    def add_user(self, name: str) -> UUID:
        user = User(name)
        self._users[user.user_id] = user
        return user.user_id

    def add_listing(self, name, description, price, duration, user_id):
        user = self.get_valid_user(user_id)
        if user is None:
            print(user_id, "not found")
            return None
        
        listing = Listing(price, duration, name, description, user)
        self._listings[listing.listing_id] = listing
        return listing.listing_id

    def add_bid(self, user_id, listing_id, price):
        user = self.get_valid_user(user_id)
        if not user:
            return None
        
        listing: Listing = self.get_valid_listing(listing_id)
        if not listing:
            return None
        
        bid = Bid(price, bidder=user)
        if not listing.is_listing_valid():
            listing.handle_bidding_close()
            return None
        
        return listing.add_new_bid(bid)

    def search(self, keyword, searchStrategy: SearchStrategy) -> List[Listing]:
        return searchStrategy.search(list(self._listings.values()), keyword)

if __name__ == "__main__":
    system = AuctionSystem()
    search = NameSearchStrategy()

    u1 = system.add_user("Noor")
    u2 = system.add_user("Nimrat")
    u3 = system.add_user("Kaur")

    l1 = system.add_listing("Pot", "Flower pot", 1000, timedelta(microseconds=1000), u1)
    l2 = system.add_listing("Pt", "Cooking pot", 1000, timedelta(microseconds=1000), u2)

    b1 = system.add_bid(u1, l2, 100)
    b2 = system.add_bid(u2, l1, 1200)
    b3 = system.add_bid(u3, l1, 1500)

    print(u1, u2, u3)
    print(l1, l2)
    print(b1, b2)

    print(system.search("Pot", search))