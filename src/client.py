from imports import *

PORT = 666
SERVER = "localhost"
#socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    return client

def send(client, message):
    messageBis= message.encode(FORMAT)
    client.send(message)

client = connect()
send(client, "testing")

