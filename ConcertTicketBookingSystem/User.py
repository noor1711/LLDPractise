from uuid import uuid4

class User:
    def __init__(self, name):
        self._name = name
        self._id = uuid4()
        # can have an Email validation

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def userId(self):
        return self._id
    
