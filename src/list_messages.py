from imports import *

#Can't bind to an under 1024 number as an unprivillege user
PORT = 6666
SERVER = socket.gethostbyname(socket.gethostname())#"localhost"
#socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    return client

def start():
    connection = connect()
    while True:
        message = connection.recv(1024).decode(FORMAT)
        print(message)


start()
