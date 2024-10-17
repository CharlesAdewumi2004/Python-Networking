from user import User
from datetime import datetime
class Message:
    def __init__(self, message : str, user : User, timeSent : str, type : str, recipient : User):
        self.message = message
        self.user = user
        self.timeSent = timeSent
        self.type = type
        self.recipient = recipient
