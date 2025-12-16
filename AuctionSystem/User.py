from uuid import uuid4, UUID
from abc import ABC, abstractmethod

class Subscriber(ABC):

    @abstractmethod
    def update(self, message: str):
        pass

class User(Subscriber):

    def __init__(self, name: str):
        self._id: UUID = uuid4()
        self._name: str = name

    @property
    def user_id(self) -> UUID:
        return self._id
    
    @property
    def name(self) -> UUID:
        return self._name
    
    def update(self, message: str):
        print(self._name, message)