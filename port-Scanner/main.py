import socket  # Import socket module for network communication.

# Define the target IP address or hostname you want to scan.
# Replace 'target_ip_or_hostname' with a real IP address or domain.
target = 'target_ip_or_hostname'

# Function to scan a port
def portScan(port):
    try:
        # Create a socket object with IPv4 (AF_INET) and TCP (SOCK_STREAM).
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to avoid long waits if the port is not responding.
        sock.settimeout(1)  # 1-second timeout for connections.

        # Try to connect to the target at the specified port.
        # If the connection is successful, the port is open.
        result = sock.connect_ex((target, port))  # connect_ex returns 0 on success (open port).
        
        # Close the socket after use to free up resources.
        sock.close()

        # Return True if the connection was successful (port is open).
        if result == 0:
            return True
        else:
            return False

    except socket.error:  # Catch any socket-related exceptions.
        return False  # If an error occurs (e.g., connection refused), return False.

# Iterate over a range of ports (1 to 1024).
for port in range(1, 1024):
    # Call the portScan function for each port.
    result = portScan(port)
    
    # If the result is True (the port is open), print that the port is open.
    if result:
        print(f"Port {port} is open")
