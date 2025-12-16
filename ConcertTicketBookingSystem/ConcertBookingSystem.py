from Concert import Concert, Seat
from User import User
from Booking import Booking
from uuid import uuid4
from typing import Dict, List
from SearchStrategy import SearchStrategy, VenueBasedSearchStrategy, ArtistBasedSearchStrategy, DateBasedSearchStrategy
from datetime import date
# notification is still left 
class ConcertBookingSystem:

    def __init__(self):
        self._concerts = {}
        self._users = {}
        self._bookings: Dict[uuid5, Booking] = {} 
    
    def addConcert(self, venue, artist, date):
        # ideally we should get num seats based on venue
        concert = Concert(venue, artist, date, 1000)
        self._concerts[concert.concertId] = concert
        return concert.concertId

    def addUser(self, name):
        user = User(name)
        self._users[user.userId] = user
        return user.userId

    def getSeatsForConcert(self, concertId, num_seats):
        concert: Concert = self._concerts.get(concertId)
        if concert is None:
            return None

        seats = concert.getSeats(num_seats)
        return seats

    def bookSeatsForConcert(self, concertId, seats: List[Seat]):
        concert: Concert = self._concerts.get(concertId)
        canOccupy = concert.occupySeats(seats)
        if canOccupy == False:
            return None
        
        bookingId = uuid4()
        booking = Booking(bookingId, seats, concertId)
        self._bookings[bookingId] = booking

        concert.occupySeats(seats)
        booking.confirm_booking()

        return bookingId
    
    def cancelBooking(self, bookingId, userId):
        booking: Booking = self._bookings.get(bookingId)
        if not booking:
           return None
        
        booking.cancel_booking()
        seats = booking._seats
        concertId = booking._concertId

        concert: Concert = self._concerts.get(concertId)
        concert.unoccupySeats(seats)

    def waitlistForConcert(self, userId, concertId, numSeats):
        concert: Concert = self._concerts.get(concertId)

        if concert is None:
            return "Invalid Concert"

        user: User = self._users.get(userId)

        if user is None:
            return "Invalid User"
        
        concert.add_to_waitlist(user, numSeats)
        return "WaitListed"
    
    def search(self, searchStrategy: SearchStrategy, keyword):
        return searchStrategy.search(list(self._concerts.values()), keyword)


if __name__ == "__main__":
    sys = ConcertBookingSystem()
    
    c1 = sys.addConcert("Delhi", "AP dhillon", date.fromisocalendar(2025, 43, 1))
    u1 = sys.addUser("Noor")
    u2 = sys.addUser("Nimrat")

    seats = sys.getSeatsForConcert(c1, 10)
    print(len(seats))
    b1 = sys.bookSeatsForConcert(c1, seats)
    print(b1)

    


    c2 = sys.addConcert("Delhi", "Karan Aujla", date.fromisocalendar(2025, 43, 1))
    c2 = sys.addConcert("Mumbai", "Coldplay", date.fromisocalendar(2025, 43, 1))
    concerts = sys.search(VenueBasedSearchStrategy(), "Delhi")
    print(len(concerts))
    print(len(sys.search(DateBasedSearchStrategy(), date.fromisocalendar(2025, 43, 1))))
