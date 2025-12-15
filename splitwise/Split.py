from User import User


class Split:
    """
    Represents a single share of an expense for a given user.
    """

    def __init__(self, user: User, value: float):
        self._user = user
        self._value = value

    @property
    def user(self) -> User:
        return self._user

    @property
    def value(self) -> float:
        return self._value

    def counterparty_split(self, counterparty: User) -> "Split":
        """
        Create the corresponding split from the counterparty's perspective.
        If this split means `self.user` owes X to counterparty,
        then the counterparty's view is that they are owed -X (and vice versa).
        """
        return Split(counterparty, -self._value)
