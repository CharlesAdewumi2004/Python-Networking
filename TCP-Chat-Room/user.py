import socket

#user of server
class User:
    def __init__(self, name  : str,clientSocket : socket , address : str):
        self.name = name
        self.clientSocket = clientSocket
        self.address = address
        
    