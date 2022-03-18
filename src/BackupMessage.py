from Imports import *

# Opening the file 'a+' to read and append mode
file = open('Message.txt', 'a+')
data = file.read(100)
if len(data) > 0:
    file.write("\n\n")
    file.write(f"{datetime.datetime.now()}\n[BEGINNING OF THE SESSION]\n")
else:
    file.write(f"{datetime.datetime.now()}\n[BEGINNING OF THE SESSION]\n")

# Can't bind to an under 1024 number as an unprivileged user
PORT = 6666
SERVER = "localhost"#socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
backup.connect(ADDRESS)


def addMessage(message):
    file.write(message + '\n')


def start():
    backup.send('Backup'.encode(FORMAT))
    enabled = True
    while enabled:
        try:
            message = backup.recv(1024).decode(FORMAT)
            if message == "Downing the server!":
                file.write("[END OF THE SESSION]\n")
                enabled = False
            elif message != 'Name' and ~message.__contains__('has joined the chat!'):
                addMessage(message)
        except:
            # Error gestion
            print("Error!")
            backup.close()
            break


start()
file.close()
os._exit(0)
