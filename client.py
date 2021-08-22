import socket
from threading import Thread
from datetime import datetime

# The IP address and PORT of the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9876
delimiter = "<DELIMITER>"

client_socket = socket.socket()
print(f"Attempting to connect to to chat server {SERVER_IP}:{SERVER_PORT}.")
client_socket.connect((SERVER_IP, SERVER_PORT))
print("Connected to the chat room. Press (q) to quit.")

# Prompt for a username for the chat room
username = input("Please enter a username: ")


# Listen for incoming messages from the server
def listen_for_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print("\n" + message)


# Create a thread to listen for and display incoming messages from the server
client_thread = Thread(target=listen_for_messages)
# Set the client thread to a daemon so that it terminates when the main thread terminates
client_thread.daemon = True
# Start the new client thread
client_thread.start()

while True:
    # Get user input to send as a message to connected clients
    message = input()
    # Exit the chatroom if the letter 'q' is sent as a message
    if message.lower() == 'q':
        break
    # Format the message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"[{timestamp}] {username}{delimiter}{message}"
    # Send the formatted message
    client_socket.send(message.encode())

# Close the socket
client_socket.close()