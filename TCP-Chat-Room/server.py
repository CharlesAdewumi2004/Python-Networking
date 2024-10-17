import threading
import socket
from user import User
from collections import deque
import pickle

class Server:
    def __init__(self):
        # Creates socket on server side, binds server IP and port number to socket, sets server to listen for connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        self.chatRecentLogs = deque(maxlen=20)
        ip = self.getHostIp()
        try:
            self.serverIp = ip  # Corrected to use actual IP
            self.port = 5555
            self.server.bind((self.serverIp, self.port))
            self.server.listen()
            print(f"Server is listening on {self.serverIp}:{self.port}")
            self.accept_connections()
        except Exception as e:
            print(e)

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
                self.users.remove(user)  # Corrected from self.clients to self.users
                user.clientSocket.close()
                break

    # Accepts clients
    def accept_connections(self):
        while True:
            clientSocket, clientAddress = self.server.accept()  # Accept new client
            newClient = clientSocket.recv(1024)
            newUser = User(newClient.decode('utf-8'), clientSocket, clientAddress)
            # Adds client to list of users
            self.users.append(newUser)
            print(f"New connection from {newUser.name}")
            # Sends recent chat logs to new client
            serializedRecentLogs = pickle.dumps(self.chatRecentLogs)
            newUser.clientSocket.sendall(serializedRecentLogs)
            # Creates a thread to handle client messages
            client_thread = threading.Thread(target=self.handle_client, args=(newUser,))
            client_thread.start()

    # Gets host IP
    def getHostIp(self):
        try:
            # Create UDP socket
            tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to Google DNS server (corrected tuple)
            tempSocket.connect(('8.8.8.8', 80))
            # Get local IP from socket
            ip = tempSocket.getsockname()[0]
            tempSocket.close()
            return ip
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    server = Server()
 
