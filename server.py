import socket
import threading
import sqlite3

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

# Connect to SQLite database
conn = sqlite3.connect('chat.db', check_same_thread=False)
cursor = conn.cursor()

# Ensure the messages table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Save message to the database
def save_message(nickname, message):
    cursor.execute("INSERT INTO messages (nickname, message) VALUES (?, ?)", (nickname, message))
    conn.commit()

# Broadcast a message to all clients and save it
def broadcast(message, nickname=None):
    if nickname:
        save_message(nickname, message.decode('utf-8'))
    for client in clients:
        try:
            client.send(message)
        except:
            # If sending fails, remove the client
            remove_client(client)

# Send the last 50 messages to a new client
def send_previous_messages(client):
    cursor.execute("SELECT nickname, message FROM messages ORDER BY timestamp DESC LIMIT 50")
    previous_messages = cursor.fetchall()
    for nickname, message in reversed(previous_messages):
        client.send(f"{nickname}: {message}".encode('utf-8'))

# Remove a client from the server
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames.pop(index)
        broadcast(f"{nickname} has left the chat!".encode('utf-8'))

# Handle communication with a client
def handle_client(client):
    while True:
        try:
            # Receive and broadcast message
            message = client.recv(1024)
            index = clients.index(client)
            nickname = nicknames[index]
            broadcast(message, nickname)
        except Exception:
            # Remove and close client if connection fails
            remove_client(client)
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

        # Send previous messages to the new client
        send_previous_messages(client)

        # Start handling thread for the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
