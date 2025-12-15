from typing import List, Dict
import uuid

from Expense import Expense
from User import User


class Group:
    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self._name = name
        # user_id -> User
        self._users: Dict[uuid.UUID, User] = {}
        self._expenses: List[Expense] = []

    def addUser(self, user: User) -> None:
        if user.id not in self._users:
            self._users[user.id] = user

    def addExpense(self, expense: Expense) -> None:
        self._expenses.append(expense)

