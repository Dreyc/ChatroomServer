import socket

# Opening the file
file = open('Message.txt', 'w')

# Can't bind to an under 1024 number as an unprivileged user
PORT = 6666
SERVER = "localhost"  # socket.gethostbyname(socket.gethostname())  # "localhost"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
backup.connect(ADDRESS)


def addMessage(message):
    file.write(message + '\n')


def start():
    backup.send('Backup'.encode(FORMAT))
    while True:
        try:
            message = backup.recv(1024).decode(FORMAT)
            if message != 'Name' and ~message.__contains__('has joined the chat!'):
                addMessage(message)
        except:
            # Error gestion
            print("Error!")
            backup.close()
            break


start()
file.close()
