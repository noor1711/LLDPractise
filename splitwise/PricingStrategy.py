from abc import ABC, abstractmethod
from typing import List, Dict

from Split import Split
from User import User


class PricingStrategy(ABC):
    
    @abstractmethod
    def calculateSplits(self, userToPercentageMapping: Dict[User, float], total: float) -> List[Split]:
        """
        Given a mapping from user to percentage of the total, return concrete splits.
        """
        pass
    

class UniformPricingStrategy(PricingStrategy):
    """
    Simple strategy: uses the provided percentages to compute each user's share.
    If all percentages are equal, this becomes an equal-split strategy.
    """

    def calculateSplits(self, userToPercentageMapping: Dict[User, float], total: float) -> List[Split]:
        ans: List[Split] = []

        for user, percentage in userToPercentageMapping.items():
            share = total * (percentage / 100.0)
            ans.append(Split(user, share))

        return ans