import socket
import csv
import os

# Define the host and port to listen on
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345  # Use a non-privileged port

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening on port", PORT)

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    # Receive the logs from the client
    received_logs = client_socket.recv(4096)  # Adjust buffer size as needed

    # Decode and process the received logs
    logs_str = received_logs.decode()
    if logs_str:
        # Parse logs into a list of lines
        logs_list = logs_str.split('\n')

        # Create a folder named "Logs" if it doesn't exist
        logs_folder = "Logs"
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)

        # Save logs to a CSV file in the "Logs" folder
        csv_file_name = f"{client_address[0]}_logs.csv"
        csv_file_path = os.path.join(logs_folder, csv_file_name)
        with open(csv_file_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for line in logs_list:
                # Split each line into columns based on delimiter (adjust as needed)
                columns = line.split(',')
                # Write each row to the CSV file
                csv_writer.writerow(columns)
        print("Logs received and saved as CSV successfully in folder: Logs")

    # Close the connection
    client_socket.close()

# Close the server socket (this will never be reached in this example)
server_socket.close()
