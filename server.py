import socket

# Define host and port
HOST = '192.168.1.44'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print("Server is listening...")

# Accept incoming connections
client_socket, client_address = server_socket.accept()

print(f"Connection from {client_address} has been established.")

# Receive data from the client
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print("Received:", data.decode())

# Close the connection
client_socket.close()
