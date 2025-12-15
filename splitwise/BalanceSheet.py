import uuid
from typing import Dict, List

from Split import Split


class BalanceSheet:
    """
    Tracks net amount owed between one user and others.
    Keys are other users' IDs, values are net deltas.
    """

    def __init__(self):
        self._amountDelta: Dict[uuid.UUID, float] = {}

    def processSplit(self, split: Split) -> None:
        otherUserId = split.user.id
        current = self._amountDelta.get(otherUserId)
        if current is None:
            self._amountDelta[otherUserId] = 0.0
        self._amountDelta[otherUserId] += split.value

    def processSplits(self, splits: List[Split]) -> None:
        for split in splits:
            self.processSplit(split)

    def settleUp(self, userId: uuid.UUID, val: float) -> None:
        current = self._amountDelta.get(userId, 0.0)
        self._amountDelta[userId] = current + val

    def printBalanceSheet(self) -> None:
        for user_id, amount in self._amountDelta.items():
            print("User", user_id, ", Amount", amount)