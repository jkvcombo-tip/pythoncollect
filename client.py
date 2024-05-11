import socket
import csv

# Define host and port
HOST = '192.168.1.44'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Define the PowerShell command to send to the server
powershell_command = "Get-EventLog -LogName System"

# Send the PowerShell command to the server
command = f"powershell:{powershell_command}"
client_socket.sendall(command.encode())

# Receive the result from the server
result = client_socket.recv(4096)

# Decode and print the result
print("Event logs from server:")
print(result.decode())

# Close the connection
client_socket.close()
