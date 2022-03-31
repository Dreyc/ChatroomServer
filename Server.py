import os

from Imports import *

# free port above 1024 (no root access needed)
# PORT = 6666
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
        if clients[client] == "Backup":
            return client
    return None


def userConnection(username):
    for client in clients:
        if clients[client] == username:
            return client
    return None


# Return all the users name and if admin addresses too
def getUsersList(admin):
    users = "[USERS LIST]\n\n"
    i = 1
    if admin:
        for client in clients:
            if clients[client] != 'Backup':
                users += f"   {i}. {clients[client]}\n"
                i += 1
            else:
                users += f"    - {clients[client]}\n"
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
                        broadcast("Downing the server!".encode(FORMAT))
                        time.sleep(1)
                        os._exit(0)
                    else:
                        print(f'{clients[connection]} asked to down the server')
                        broadcast("Downing the server!".encode(FORMAT))
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
                        connection.send("[BACKUP CLEARED]".encode(FORMAT))
                    else:
                        connection.send("[NO BACKUP ENABLED]".encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            elif message.lower() == "!users":
                if clients[connection].lower().__contains__("admin"):
                    connection.send(getUsersList(True).encode(FORMAT))
                else:
                    connection.send(getUsersList(False).encode(FORMAT))
            elif message.lower() == "!emotes":
                #Link to the emote list
                connection.send("[EMOTE LIST]".encode(FORMAT))
            elif message.startswith("@"):
                splitted = message.split()
                username = splitted[0]
                if clients[connection] == username[1:]:
                    connection.send('[CANNOT SEND MESSAGE TO YOURSELF]'.encode(FORMAT))
                else:
                    mpConnection = userConnection(username[1:])
                    if mpConnection is not None:
                        mpConnection.send((f'[DM] {clients[connection]} : ' + message[(len(username)+1):]).encode(FORMAT))
                        connection.send((f'[DM] {clients[connection]} : ' + message).encode(FORMAT))
                    else:
                        connection.send((f'[{username} NOT FOUND]\nMessage : ' + message[(len(username)+1):]).encode(FORMAT))
            elif message == "[KICKED]":
                print(f'{clients[connection]} has been kicked off the server')
                connected = False
            elif message == "!kickall":
                if clients[connection].lower().__contains__("admin"):
                    print(f'{clients[connection]} kicked all the muggles')
                    broadcast(f"{clients[connection]} casted AVADA KEDAVRA killing all the muggles in the area".encode(FORMAT))
                    for client in clients:
                        if not clients[client].lower().__contains__("admin"):
                            client.send("[KICKED]".encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            elif message.startswith("!kick"):
                if clients[connection].lower().__contains__("admin"):
                    splitted = message.split()
                    username = splitted[1]
                    uConnection = userConnection(username)
                    if username == 'Backup' or username.lower().__contains__("admin"):
                        connection.send("[CANNOT BAN SUPER USER]".encode(FORMAT))
                    elif uConnection is not None:
                        uConnection.send("[KICKED]".encode(FORMAT))
                        broadcast(f'[{clients[uConnection]} has been kicked by {clients[connection]}]'.encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
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
