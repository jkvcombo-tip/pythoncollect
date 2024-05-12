import socket
import subprocess

# Define the server's IP address and port
SERVER_HOST = '192.168.1.44'  # Replace 'remote_machine_ip' with the actual IP address of the server
SERVER_PORT = 12345  # Use the same port as defined in the server

# Define the PowerShell command to retrieve system logs
powershell_command = "Get-EventLog -LogName System"

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Execute the PowerShell command to retrieve system logs
try:
    logs = subprocess.check_output(["powershell", "-Command", powershell_command], shell=True)
    # Send the logs to the server
    client_socket.sendall(logs)
except subprocess.CalledProcessError as e:
    print("Error retrieving logs:", e)

# Close the connection
client_socket.close()
