from uuid import uuid4

from typing import List, Dict
from User import User
from Group import Group
from Expense import Expense
from Split import Split
from PricingStrategy import PricingStrategy, UniformPricingStrategy
from BalanceSheet import BalanceSheet

class SplitService:

    def __init__(self, splitStrategy: PricingStrategy):
        self._users: Dict[str, User] = {}
        self._groups: Dict[str, Group] = {}
        self._balanceSheets: Dict[str, BalanceSheet] = {}
        self._pricingStrategy = splitStrategy
    
    def addUser(self, name, email):
        # TODO: add check for email not being present
        user = User(name, email)
        self._users[user.id] = user
        self._balanceSheets[user.id] = BalanceSheet()
        return user.id
    
    def addGroup(self, name):
        group = Group(name)
        self._groups[group.id] = group
        return group.id

    def addUserToGroup(self, groupId, userId):
        if userId in self._users and groupId in self._groups:
            group = self._groups[groupId]
            user = self._users[userId]
            group.addUser(user)

    def addExpenseToGroup(self, name: str, paidByUserId: str, groupId: str,  total: int, userToPercentageMapping: Dict):
        # we need to calculate the splits
        
        splits: List[Split] = self._pricingStrategy.calculateSplits(userToPercentageMapping, total)
        expense = Expense(name, paidByUserId, total, splits)
        
        group = self._groups.get(groupId)
        group.addExpense(expense)

        # we need to add these to the subsequent balance sheets of all the users 
        balanceSheet = self._balanceSheets[paidByUserId]
        balanceSheet.processSplits(splits)
        
        for split in splits:
            user = split._user
            value = split._value

            balanceSheet = self._balanceSheets[user]
            balanceSheet.processSplit(Split(paidByUserId, -value))
        
    def settleUp(self, fromUser, toUser, val):
        sheet1 = self._balanceSheets.get(fromUser)
        sheet2 = self._balanceSheets.get(toUser)

        sheet1.settleUp(toUser, -val)
        sheet2.settleUp(fromUser, val)
    
    def printBalanceSheet(self, userId):
        balanceSheet = self._balanceSheets[userId]
        balanceSheet.printBalanceSheet()

if __name__ == "__main__":

    pricingStrategy = UniformPricingStrategy()
    ss = SplitService(pricingStrategy)

    user1 = ss.addUser("noor", "ngi")
    user2 = ss.addUser("nimrat", "nni")
    user3 = ss.addUser("kaur", "nki")

    group1 = ss.addGroup("yoyo")
    print(user1, user2)

    ss.addUserToGroup(group1, user1)
    ss.addUserToGroup(group1, user2)
    ss.addUserToGroup(group1, user3)
    ss.addExpenseToGroup("Yuki", user1, group1, 2000, {user2: 50, user3: 50})
    print(ss.printBalanceSheet(user1))
    print(ss.printBalanceSheet(user2))
    print(ss.printBalanceSheet(user3))