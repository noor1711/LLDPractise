import uuid

class User:
    def __init__(self, name, email):
        self.id = uuid.uuid4()
        self._name = name
        self._email = email
    