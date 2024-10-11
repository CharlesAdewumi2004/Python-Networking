import socket
import threading

class Client:
    def __init__(self, server_ip, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.name = input("Enter name: ")

        # Try to connect to the server
        try:
            self.client.connect((self.server_ip, self.server_port))
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
            self.client.send(self.name.encode('utf-8'))
        except Exception as e:
            print(f"Connection error: {e}")
            return
        
        # Start threads for sending and receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

    def receive_messages(self):
        # Continuously listen for incoming messages from the server
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')  # Receive message
                if message:
                    print(f"Server: {message}")  # Display the message from the server
                else:
                    print("Server disconnected")
                    self.client.close()
                    break
            except:
                print("Error receiving message.")
                self.client.close()
                break

    def send_messages(self):
        # Continuously send messages to the server
        while True:
            message = input("You: ")
            try:
                self.client.send(message.encode('utf-8'))  # Send message to the server
            except:
                print("Error sending message.")
                self.client.close()
                break

# Connect to the server
if __name__ == "__main__":
    client = Client('192.168.56.1', 5555)
