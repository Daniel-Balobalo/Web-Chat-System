import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5555         # Port to listen on

# Start server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# List to keep track of connected clients
clients = []
nicknames = []

# Broadcast a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle communication with a client
def handle_client(client):
    while True:
        try:
            # Receive and broadcast message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close client if connection fails
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat!".encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accept new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Get and save nickname for the client
        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        # Start handling thread for each client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
