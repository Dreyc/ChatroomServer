from Imports import *

# free port above 1024 (no root access needed)
PORT = 6666
SERVER = "localhost"  # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
# True if backup enabled
BACKUP = False
# List of clients and their names
# clients, names = [], []
# Connection : Name
clients = dict()

# Creating a socket for the server and bind the
# address of the server in the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


# Return the address of the backup connection
def backupConnection():
    for client in clients:
        if clients[client] == "backup":
            return client
    return None


# Return all the users name and if admin addresses too
def getUsersList(admin):
    users = "[USERS LIST]\n\n"
    i = 1
    if admin:
        for client in clients:
            users += f"   {i}. {clients[client]}\n"
            i += 1
    else:
        for client in clients:
            if clients[client] != 'Backup':
                users += f"   {i}. {clients[client]}\n"
                i += 1
    return users


# Send the message to other users
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle incomming messages
def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address}\n")

    try:
        connected = True
        while connected:
            # received message
            message = connection.recv(1024).decode(FORMAT)

            if message == DISCONNECT_MESSAGE or message.lower() == "quit":
                print(f'{clients[connection]} Deconnected!')
                broadcast(f'{clients[connection]} Deconnected!'.encode(FORMAT))
                connected = False
            elif message.lower() == "!serveroff" or message.lower() == "!serveroff/yes":
                if clients[connection].lower().__contains__("admin"):
                    if message.lower() == "!serveroff/yes":
                        print(f'{clients[connection]} asked to down the server')
                        broadcast("Downing the server!\nCleaning the Backup : [Yes] / No".encode(FORMAT))
                        print("[BACKUP CLEARED]")
                        time.sleep(1)
                        os._exit(0)
                    else:
                        print(f'{clients[connection]} asked to down the server')
                        broadcast("Downing the server!\nCleaning the Backup : Yes / [No]".encode(FORMAT))
                        print("[BACKUP SAVED]")
                        time.sleep(1)
                        os._exit(0)
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            elif message.lower() == "!nbconnections":
                if BACKUP:
                    connection.send(f"[{threading.active_count() - 2} active connection(s)]".encode(FORMAT))
                else:
                    connection.send(f"[{threading.active_count() - 1} active connection(s)]".encode(FORMAT))
            elif message.lower() == "!wizz":
                broadcast(f"{clients[connection]} wizzed!".encode(FORMAT))
                broadcast("wizz".encode(FORMAT))
            elif message.lower() == "!clearbackup":
                if clients[connection].lower().__contains__("admin"):
                    if backupConnection() is not None:
                        backupConnection().send("!clearbackup".encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            elif message.lower() == "!users":
                if clients[connection].lower().__contains__("admin"):
                    connection.send(getUsersList(True).encode(FORMAT))
                else:
                    connection.send(getUsersList(False).encode(FORMAT))
            else:
                broadcast(message.encode(FORMAT))
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
            print(f"New connection's name : {name}")

            # To every user connected
            broadcast(f"{name} has joined the chat!\n".encode(FORMAT))
            # To the user
            connection.send("Connected!\n".encode(FORMAT))
        else:
            BACKUP = True
            print('[BACKUP ENABLED]')
        # Starting the Thread
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        # Print number of active connections
        print(f"Active connections : {threading.active_count() - 1}")


# Launching the chat session
start()
os._exit(0)
