import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # Server IP address (localhost here)
PORT = 5555         # Server port

nickname = input("Choose a nickname: ")

# Start client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close connection on error
            print("An error occurred!")
            client.close()
            break

# Send messages to the server
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads for sending and receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
