from User import User
from Split import Split
from typing import Dict, List

# this will be a user to user mapping
class BalanceSheet: 
    def __init__(self):
        self._amountDelta: Dict[str, float] = {}
    
    def processSplit(self, split: Split):
        otherUserId = split._user
        amountOwed = self._amountDelta.get(otherUserId)
        if not amountOwed:
            self._amountDelta[otherUserId] = 0
        self._amountDelta[otherUserId] += split._value
    
    def processSplits(self, splits: List[Split]):
        for split in splits:
            self.processSplit(split)

    def settleUp(self, userId, val):
        self._amountDelta[userId] += val
    
    def printBalanceSheet(self):
        for user in self._amountDelta:
            print("User", user, ", Amount", self._amountDelta[user])