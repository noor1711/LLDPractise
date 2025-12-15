from User import User
from Split import Split
from typing import Dict, List


class Expense:
    def __init__(self, name, paidBy: str, total, splits: List[Split]):
        self._name = name
        self._paid_by = paidBy
        self._total = total
        self._splits = splits