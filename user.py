class user:
    def __init__(self, first_name, last_name, username, password):
        self.ID = ""  # ID not needed for inserting into database and can be mapped to the object later
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password  # The real thing would have hashed passwords but we probably don't need them for our purposes
