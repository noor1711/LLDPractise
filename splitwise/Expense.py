from typing import List

from User import User
from Split import Split


class Expense:
    """
    Represents an expense paid by one user and split among others.
    """

    def __init__(self, name: str, paidBy: User, total: float, splits: List[Split]):
        self._name = name
        self._paid_by = paidBy
        self._total = float(total)
        self._splits = splits

    @property
    def name(self) -> str:
        return self._name

    @property
    def paid_by(self) -> User:
        return self._paid_by

    @property
    def total(self) -> float:
        return self._total

    @property
    def splits(self) -> List[Split]:
        return self._splits