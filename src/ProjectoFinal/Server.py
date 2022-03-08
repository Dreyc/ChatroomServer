import socket
import threading

# free port above 1024 (no root access needed)
PORT = 6666
SERVER = "localhost"  # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# List of clients and their names
# clients, names = [], []
# Connection : Name
clients = dict()

# Creating a socket for the server and bind the
# address of the server in the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


# Send the message to other users
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle incomming messages
def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address}")

    try:
        connected = True
        while connected:
            # received message
            message = connection.recv(1024)
            print(message)
            broadcast(message)

            if message == DISCONNECT_MESSAGE:
                print(f'{clients[connection]} Deconnected!')
                broadcast(f'{clients[connection]} Deconnected!'.encode(FORMAT))
                connected = False
    finally:
        del clients[connection]
        connection.close()


# start the chat
def start():
    # Sequence for anonymous name
    seq = 0
    # Server is on and print the IP
    print(f"[SERVER STARTED][{SERVER}]")
    # Listenning for connections
    server.listen()
    while True:
        connection, address = server.accept()
        connection.send("Name".encode(FORMAT))
        name = connection.recv(1024).decode(FORMAT)

        # Adding the client and his name to the list
        # clients.append(connection)
        # names.append(name)
        clients[connection] = name

        if name != 'Backup':
            print(f"Your name : {name}")

            # To every user connected
            broadcast(f"{name} has joined the chat!\n".encode(FORMAT))
            # To the user
            connection.send("Connected!\n".encode(FORMAT))
        else:
            print('[BACKUP ENABLED]')
        # Starting the Thread
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        # Print number of active connections
        print(f"Active connections : {threading.active_count() - 1}")


# Launching the chat session
start()
