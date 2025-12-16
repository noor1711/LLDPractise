from Concert import Concert
from typing import List
from abc import ABC, abstractmethod
from datetime import date

class SearchStrategy(ABC):

    @abstractmethod
    def search(self, concerts: List[Concert], keyword: str):
        pass

class VenueBasedSearchStrategy(SearchStrategy):

    def search(self, concerts: List[Concert], keyword: str):
        return list(filter(lambda concert: concert.venue.find(keyword) != -1, concerts))
    

class ArtistBasedSearchStrategy(SearchStrategy):

    def search(self, concerts: List[Concert], keyword: str):
        return list(filter(lambda concert: concert.artist.find(keyword) != -1, concerts))

class DateBasedSearchStrategy(SearchStrategy):

    def search(self, concerts: List[Concert], date: date):
        return list(filter(lambda concert: concert.date == date, concerts))
