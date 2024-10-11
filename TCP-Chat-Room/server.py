import threading
import socket

class Server:
    def __init__(self):
        # creates socket on server side/binds server ip and port numer to socket/sets server to listen for cnnections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.clinetName = []
        self.serverIp = '192.168.234.128'
        self.port = 5555
        self.server.bind((self.serverIp, self.port))
        self.server.listen()
        print(f"Server is listening on {self.serverIp} : {self.port}")
        
        self.accept_connections()

    def broadcast(self, message, client_socket):
        # Send a message to all connected clients except the sender
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    # Remove client if there is an issue
                    self.clients.remove(client)
    #handles messages from client
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)  # Receive message from client
                if not message:
                    # If no message is received, remove the client
                    print("Client disconnected")
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                else:
                    # Broadcast the received message to other clients
                    print(f"{self.clinetName[self.clients.index(client_socket)]}: {message.decode('utf-8')}")
                    self.broadcast(message, client_socket)
            except:
                # Handle any client disconnection errors
                self.clients.remove(client_socket)
                client_socket.close()
                break
    #accepts clients
    def accept_connections(self):
        while True:
            client_socket, client_address = self.server.accept()  # Accept new client
            newClient = client_socket.recv(1024)
            #adds client to list of clinets and the name of th new client to clinetNames
            self.clinetName.append(newClient.decode('utf-8'))
            self.clients.append(client_socket) 
            print(f"New connection from {newClient.decode('utf-8')}")
            #creates a thread to handle client messages
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = Server()   
