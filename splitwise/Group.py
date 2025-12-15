from typing import List, Dict
from Expense import Expense
from User import User
import uuid

class Group:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self._name = name
        self._users : Dict[User] = {}
        self._expenses : List[Expense] = []
    
    def addUser(self, user: User):
        if not self._users.get(user.id):
            self._users[user.id] = user
    
    def addExpense(self, expense: Expense):
        self._expenses.append(expense)
    
