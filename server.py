import socket
from threading import Thread

# The IP address and PORT of the remote server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9876

# Specify a delimiter to separate a client's name and message
delimiter = "<DELIMITER>"

# Initialize a list of connected client sockets
client_sockets = set()

# Create a TCP socket
server_socket = socket.socket()

# Make the port for the socket reusable
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the IP address and Port we defined earlier
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
server_socket.listen()
print("Chat server has started.")
print(f"Listening for connections on {SERVER_IP}:{SERVER_PORT}.")


# Repeatedly listen for a message from the client socket and
# broadcast received messages to all other connected clients.
def listen_for_client(client_socket):
    while True:
        try:
            # Listen for a message from the client socket
            message = client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Error: {e}")
            # The client is no longer connected so remove it from
            # the set of clients to broadcast to
            client_sockets.remove(client_socket)
        else:
            # Replace the delimiter with a format token
            # when a message is received
            message = message.replace(delimiter, ": ")
        # Send the message to all client sockets
        for cs in client_sockets:
            cs.send(message.encode())


while True:
    # Continuously listen for new connections
    client_socket, client_address = server_socket.accept()
    print(f"Client {client_address} has connected to the chat.")
    # Add newly connected clients to the list of connected clients
    client_sockets.add(client_socket)
    # Create a new thread to listen to messages for the newly connected client
    client_thread = Thread(target=listen_for_client, args=(client_socket,))
    # Set the client thread to a daemon so that it terminates when the main thread terminates
    client_thread.daemon = True
    # Star the new client thread
    client_thread.start()

# Close client sockets
for cs in client_sockets:
    cs.close()

# Close the chat server socket
server_socket.close()
