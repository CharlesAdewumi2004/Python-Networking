import threading
import socket
from user import User
from collections import deque
import pickle

class Server:
    def __init__(self):
        # creates socket on server side/binds server ip and port numer to socket/sets server to listen for cnnections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        self.chatRecentLogs = deque(maxlen=20)
        self.serverIp = '192.168.0.38'
        self.port = 5555
        self.server.bind((self.serverIp, self.port))
        self.server.listen()
        print(f"Server is listening on {self.serverIp} : {self.port}")
        
        self.accept_connections()

    def broadcast(self, message, clientSocket):
        # Send a message to all connected clients except the sender
        for user in self.users:
            if user.clientSocket != clientSocket:
                try:
                    user.clientSocket.send(message)
                except:
                    # Remove client if there is an issue
                    self.users.remove(user)
    # Handles messages from client
    def handle_client(self, user):
        while True:
            try:
                message = user.clientSocket.recv(1024)  # Receive message from client
                if not message:
                    # If no message is received, remove the client
                    print(f"Client {user.name} disconnected")
                    self.users.remove(user)
                    user.clientSocket.close()
                    break
                else:
                    # Broadcast the received message to other clients
                    print(f"{message.decode('utf-8')}")
                    self.chatRecentLogs.append(message.decode('utf-8'))
                    self.broadcast(message, user.clientSocket)
            except:
                # Handle any client disconnection errors
                self.clients.remove(user.clientSocket)
                user.clientSocket.close()
                break
    #accepts clients
    def accept_connections(self):
        while True:
            clientSocket, clientAddress = self.server.accept()  # Accept new client
            newClient = clientSocket.recv(1024)
            newUser = User(newClient.decode('utf-8'), clientSocket, clientAddress)
            #adds client to list of clinets and the name of th new client to clinetNames
            self.users.append(newUser)
            print(f"New connection from {newUser.name}")
            #creates a thread to handle client messages
            serializedRecentLogs = pickle.dumps(self.chatRecentLogs)
            newUser.clientSocket.sendall(serializedRecentLogs)
            client_thread = threading.Thread(target=self.handle_client, args=(newUser,))
            client_thread.start()

if __name__ == "__main__":
    server = Server()   
