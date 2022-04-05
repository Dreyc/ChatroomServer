###################################################################
# Mikail YILMAZ, Ouassim MEFTAH, Hilmi CELAYIR & Quentin BERTRAND #
###################################################################
from Imports import *

##########################################
# All the time.sleep are to avoid errors #
##########################################


# True if backup enabled
BACKUP = False

# Dictionary of the clients connections and their names
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

# Return the connection corresponding to the username
# None if not found
def userConnection(username):
    for client in clients:
        if clients[client] == username:
            return client
    return None

# return a string with a list of all command
# depends on if you're admin or not
def commands(admin):
    command = ""
    if admin:
        command += "[ADMIN COMMAND LIST]\n\n"
        for c in commandList:
            command += f"   - {c}\n"
        command += "   - a@[user]\n   - @[user]"
    else:
        command += "[COMMAND LIST]\n\n"
        for c in commandListUser:
            command += f"   - {c}\n"
    return command

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


# Send the message to all users
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
            # the code below correspond of all the commands
            # and actions of them
            if message.lower() == "!quit":
                print(f'{clients[connection]} Deconnected!')
                broadcast(f'{clients[connection]} Deconnected!'.encode(FORMAT))
                connected = False
            # turns down the server and disconnect all the users
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
            # return the number of connections, without the backup one
            elif message.lower() == "!nbconnections":
                if BACKUP:
                    connection.send(f"[{threading.active_count() - 2} active connection(s)]".encode(FORMAT))
                else:
                    connection.send(f"[{threading.active_count() - 1} active connection(s)]".encode(FORMAT))
            # play the wizz sound to all users
            elif message.lower() == "!wizz":
                broadcast(f"{clients[connection]} wizzed!".encode(FORMAT))
                time.sleep(0.5)
                broadcast("wizz".encode(FORMAT))
            # if admin, clear all the logs of the backup
            elif message.lower() == "!clearbackup":
                if clients[connection].lower().__contains__("admin"):
                    if backupConnection() is not None:
                        backupConnection().send("!clearbackup".encode(FORMAT))
                        connection.send("[BACKUP CLEARED]".encode(FORMAT))
                    else:
                        connection.send("[NO BACKUP ENABLED]".encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            # return the list of all the users, if admin backup is in it
            elif message.lower() == "!users":
                if clients[connection].lower().__contains__("admin"):
                    connection.send(getUsersList(True).encode(FORMAT))
                else:
                    connection.send(getUsersList(False).encode(FORMAT))
            # Direct Messages
            elif message.startswith("@"):
                # Slitting the message to separate the username from the message
                splitted = message.split()
                # retrieve the usernam : @example
                username = splitted[0]
                # so the message isn't empty
                if len(splitted) > 1:
                    if clients[connection] == username[1:]:
                        connection.send('[CANNOT SEND MESSAGE TO YOURSELF]'.encode(FORMAT))
                    else:
                        # username[1:] to crop the @ of the username to find it
                        mpConnection = userConnection(username[1:])
                        if mpConnection is not None:
                            mpConnection.send((f'[DM] {clients[connection]} : ' + message[(len(username)+1):]).encode(FORMAT))
                            connection.send((f'[DM] {clients[connection]} : ' + message).encode(FORMAT))
                        else:
                            connection.send((f'[ {username[1:]} NOT FOUND]\nMessage : ' + message[(len(username)+1):]).encode(FORMAT))
                else:
                    connection.send("[EMPTY DM]".encode(FORMAT))
            # Anonymous Direct Messages
            elif message.startswith("a@"):
                # Same as Direct Messages code above
                splitted = message.split()
                username = splitted[0]
                if len(splitted) > 1:
                    if clients[connection] == username[2:]:
                        connection.send('[CANNOT SEND MESSAGE TO YOURSELF]'.encode(FORMAT))
                    else:
                        mpConnection = userConnection(username[2:])
                        if mpConnection is not None:
                            mpConnection.send((f'[DM] ' + message[(len(username)+1):]).encode(FORMAT))
                            connection.send((f'[DM] {clients[connection]} : ' + message).encode(FORMAT))
                        else:
                            connection.send((f'[ {username[2:]} NOT FOUND]\nMessage : ' + message[(len(username)+1):]).encode(FORMAT))
                else:
                    connection.send("[EMPTY DM]".encode(FORMAT))
            # Message to end the connection of a client who has been kciked
            elif message == "[KICKED]":
                print(f'{clients[connection]} has been kicked off the server')
                connected = False
            # if admin, kick all the users that aren't admin or backup
            elif message == "!kickall":
                if clients[connection].lower().__contains__("admin"):
                    # Reference to Harry Potter
                    print(f'{clients[connection]} kicked all the muggles')
                    broadcast(f"{clients[connection]} casted AVADA KEDAVRA !\nKilling all the muggles in the area".encode(FORMAT))
                    time.sleep(0.1)
                    for client in clients:
                        if not clients[client].lower().__contains__("admin"):
                            client.send("[KICKED]".encode(FORMAT))
                else:
                    connection.send("[ACCESS DENIED]".encode(FORMAT))
            # to kick for the server a person : !kick user
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
            # Print all the command that the user can call
            elif message == "!help":
                if clients[connection].lower().__contains__("admin"):
                    connection.send(commands(True).encode(FORMAT))
                else:
                    connection.send(commands(False).encode(FORMAT))
            # send the message to all the clients connected
            else:
                broadcast(message.encode(FORMAT))
    finally:
        # if a connection is stopped, delete the user from the
        # dictionary and close the connection
        del clients[connection]
        connection.close()

# if the name of the new client contains "admin"
# the password has to be the right one otherwise
# the new client isn't allowed to connect
def admin(name, connection):
    if name.lower().__contains__("admin"):
        connection.send("Password".encode(FORMAT))
        password = connection.recv(1024).decode(FORMAT)
        if password != PASSWORD:
            connection.send("[NOPE]".encode(FORMAT))
            return False
    return True

# start the chat
def start():
    # Server is on and print the IP
    print(f"[SERVER STARTED][{SERVER}]")
    # Listenning for connections
    server.listen()
    while True:
        # connection socket and address of the new client
        connection, address = server.accept()
        # request the name
        connection.send("Name".encode(FORMAT))
        # decode the message to save the name
        name = connection.recv(1024).decode(FORMAT)
        if admin(name, connection):
            # Adding the client and his name to the list
            # clients.append(connection)
            # names.append(name)
            clients[connection] = name
            # Sinon les messages ne s'affichent pas pour le nouveau client
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
# End the script
os._exit(0)
