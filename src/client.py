from imports import *

#Can't bind to an under 1024 number as an unprivillege user
PORT = 6666
SERVER = "10.3.141.1" #"localhost"
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
    client.send(messageBis)

def start():
    answer = input("Would you like to connect (ye/no) ?")
    if answer.lower() != "yes": #.lower() to set the answer to lower case
        return

    connection = connect()
    while True:
        message = input("Message (q for quit): \n")
        if message.lower() == "q":
            break
        send(connection, message)
    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1) #second
    print("Disconnected")


start()
