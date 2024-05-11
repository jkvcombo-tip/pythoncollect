import socket
import subprocess
import csv
import os

# Define host and port
HOST = '192.168.1.44'
PORT = 12345
OUTPUT_FOLDER = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print("Server is listening...")

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established.")

    # Receive the command from the client
    command = client_socket.recv(256).decode()
    print("Received command:", command)
    
    # Execute the PowerShell script
    if command.startswith("powershell:"):
        script = command[len("powershell:"):]
        try:
            result = subprocess.check_output(["powershell.exe", "-Command", script], shell=True)
            # Save the result to a CSV file
            ip_address = client_address[0]
            filename = os.path.join(OUTPUT_FOLDER, f"{ip_address}.csv")
            save_to_csv(result.decode().strip(), filename)
            print(f"Result saved to {filename}")
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing PowerShell script: {e}"
            print(error_message)
    else:
        print("Invalid command.")

    # Close the connection
    client_socket.close()
