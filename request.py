class request:
    'This is the main object that stores information about somones request'
    def __init__(self, kind, value, user, date):
        self.kind = kind # options: "search, url, IPFS hash, git URL
        self.value = value # the value associated with the type
        self.user = user # The user associated with this request. We can make a user object later if we feel like it
        self.date = date # This should be a date-time object
        self.downloaded_status = False # This is not included in the constructor because state should always be false when starting
        self.file_location = "" # There is no downloaded location when the object is created
    def set_downloaded_status(self, state):
        self.state = state # Should be a boolean
    def set_file_location(self, loc):
        self.location = loc # Is there a file object that would be better to use than a string?
