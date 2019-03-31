import uuid
class User:
    def __init__(self, first_name, last_name, username, password):
        self.ID = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password  # in hashed form
