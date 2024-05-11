import socket
import subprocess
import csv
import os
import threading
import signal

# Define host and port
HOST = '192.168.1.44'
PORT = 12345
OUTPUT_FOLDER = "server_output"

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Event Log"])
        writer.writerow([data])

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")
    # Receive the command from the client
    command = client_socket.recv(4096).decode()
    print("Received command:", command)
    
    # Execute the PowerShell script
    if command.startswith("powershell:"):
        script = command[len("powershell:"):]
        try:
            result = subprocess.check_output(["powershell.exe", "-Command", script], shell=True)
            # Send the result back to the client
            client_socket.sendall(result)
            # Receive result from client and save as CSV file
            received_data = result.decode()
            # Adjusted to replace underscores with dots in the IP address
            client_ip = client_address[0].replace('_', '.')  # Replace '_' with '.' for filename
            output_file = os.path.join(OUTPUT_FOLDER, f'{client_ip}_event_logs.csv')
            save_to_csv(received_data, output_file)
            print(f"Event logs saved to {output_file}")
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing PowerShell script: {e}"
            client_socket.sendall(error_message.encode())
    else:
        print("Invalid command.")

    # Close the connection
    client_socket.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print("Server is listening...")

# Function to handle shutdown
def shutdown_server(signum, frame):
    print("Exiting server... Ctrl+C successful")
    server_socket.close()
    exit()

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, shutdown_server)

try:
    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    shutdown_server(signal.SIGINT, None)
