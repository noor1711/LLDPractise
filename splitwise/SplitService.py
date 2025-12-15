import uuid
from typing import List, Dict

from User import User
from Group import Group
from Expense import Expense
from Split import Split
from PricingStrategy import PricingStrategy, UniformPricingStrategy
from BalanceSheet import BalanceSheet


class SplitService:

    def __init__(self, splitStrategy: PricingStrategy):
        # id -> entity
        self._users: Dict[uuid.UUID, User] = {}
        self._groups: Dict[uuid.UUID, Group] = {}
        self._balanceSheets: Dict[uuid.UUID, BalanceSheet] = {}
        self._pricingStrategy = splitStrategy
    
    def addUser(self, name: str, email: str) -> User:
        """
        Create a new user and corresponding balance sheet.
        """
        user = User(name, email)
        self._users[user.id] = user
        self._balanceSheets[user.id] = BalanceSheet()
        return user
    
    def addGroup(self, name: str) -> Group:
        group = Group(name)
        self._groups[group.id] = group
        return group

    def addUserToGroup(self, groupId: uuid.UUID, userId: uuid.UUID) -> None:
        if userId in self._users and groupId in self._groups:
            group = self._groups[groupId]
            user = self._users[userId]
            group.addUser(user)

    def addExpenseToGroup(
        self,
        name: str,
        paidByUserId: uuid.UUID,
        groupId: uuid.UUID,
        total: float,
        userToPercentageMapping: Dict[uuid.UUID, float],
    ) -> None:
        """
        Add an expense to a group, compute splits, and update all balance sheets.
        userToPercentageMapping maps user IDs to their percentage share.
        """
        group = self._groups.get(groupId)
        paid_by_user = self._users.get(paidByUserId)
        if group is None or paid_by_user is None:
            raise ValueError("Invalid group or paying user")

        # Convert mapping from user IDs to User objects for pricing strategy
        user_percentage_by_user: Dict[User, float] = {}
        for user_id, percentage in userToPercentageMapping.items():
            user = self._users.get(user_id)
            if user is None:
                raise ValueError(f"Invalid user id in split: {user_id}")
            user_percentage_by_user[user] = percentage

        splits: List[Split] = self._pricingStrategy.calculateSplits(
            user_percentage_by_user, float(total)
        )
        expense = Expense(name, paid_by_user, total, splits)

        group.addExpense(expense)

        # Update paying user's balance sheet with what others owe them
        payer_sheet = self._balanceSheets[paid_by_user.id]
        payer_sheet.processSplits(splits)
        
        # For each participant, update their sheet with the counterparty view
        for split in splits:
            user = split.user
            value = split.value

            user_sheet = self._balanceSheets[user.id]
            counter_split = split.counterparty_split(paid_by_user)
            user_sheet.processSplit(counter_split)
        
    def settleUp(self, fromUser: uuid.UUID, toUser: uuid.UUID, val: float) -> None:
        sheet1 = self._balanceSheets.get(fromUser)
        sheet2 = self._balanceSheets.get(toUser)
        if sheet1 is None or sheet2 is None:
            raise ValueError("Invalid users for settleUp")

        sheet1.settleUp(toUser, -val)
        sheet2.settleUp(fromUser, val)
    
    def printBalanceSheet(self, userId: uuid.UUID) -> None:
        balanceSheet = self._balanceSheets[userId]
        balanceSheet.printBalanceSheet()


if __name__ == "__main__":

    pricingStrategy = UniformPricingStrategy()
    ss = SplitService(pricingStrategy)

    user1 = ss.addUser("noor", "ngi")
    user2 = ss.addUser("nimrat", "nni")
    user3 = ss.addUser("kaur", "nki")

    group1 = ss.addGroup("yoyo")
    print(user1.id, user2.id)

    ss.addUserToGroup(group1.id, user1.id)
    ss.addUserToGroup(group1.id, user2.id)
    ss.addUserToGroup(group1.id, user3.id)

    ss.addExpenseToGroup(
        "Yuki",
        user1.id,
        group1.id,
        2000,
        {user2.id: 50, user3.id: 50},
    )
    ss.printBalanceSheet(user1.id)
    ss.printBalanceSheet(user2.id)
    ss.printBalanceSheet(user3.id)