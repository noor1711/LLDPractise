from abc import ABC, abstractmethod
from Listing import Listing
from typing import List

class SearchStrategy(ABC):

    @abstractmethod
    def search(self, listings: List[Listing], keyword):
        pass

class NameSearchStrategy(SearchStrategy):

    def search(self, listings: List[Listing], keyword) -> List[Listing]:
        return list(filter(lambda listing: listing.name.find(keyword) != -1, listings))