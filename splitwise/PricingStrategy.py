from abc import ABC, abstractmethod
from typing import List, Dict
from Split import Split

class PricingStrategy(ABC):
    
    @abstractmethod
    def calculateSplits(self, userToPercentageMapping, total) -> List[Split]:
        pass


class UniformPricingStrategy(PricingStrategy):

    def calculateSplits(self, userToPercentageMapping: Dict[str, float], total) -> List[Split]:
        totalUsers = len(userToPercentageMapping)
        ans = []

        for user in userToPercentageMapping:
            split = Split(user, total / totalUsers)
            ans.append(split)
        
        return ans