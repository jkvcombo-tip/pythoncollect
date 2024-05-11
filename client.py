import socket

# Define host and port
HOST = '192.168.1.44'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send data to the server
message = "Hello, server!"
client_socket.sendall(message.encode())

# Close the connection
client_socket.close()
