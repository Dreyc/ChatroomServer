from imports import *

PORT = 666
SERVER = "localhost"
#socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

clients = set()
clients_lock = threading.Lock()

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} Connected")

    try:
        connected = True
        while connected:
            message = connection.recv(1024).decode(FORMAT)
            if not message:
                break
            if message == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{address}] {message}")
            #Send the message to all the clients
            with clients_lock:
                for c in clients:
                    c.sendall(f"[{address}] {message}".encode(FORMAT))

    finally:
        with clients_lock:
            clients.remove(connection)
        connection.close()

def start():
    print('[SERVER STARTED]')
    server.listen()
    while True:
        connection, address = server.accept()
        with clients_lock:
            clients.add(connection)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

start()
