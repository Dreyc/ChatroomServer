###################################################################
# Mikail YILMAZ, Ouassim MEFTAH, Hilmi CELAYIR & Quentin BERTRAND #
###################################################################
from Imports import *

# Creating and connecting the backup to the server
backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
backup.connect(ADDRESS)

# Initialize the backup by writing down in the Message.txt file
# the datetime
def startBackup():
    # Open the file in append + read mode
    file = open('Message.txt', 'a+')
    # Reading the 100 first char to know if the file is empty or not
    data = file.read(100)
    # If it isn't empty
    if len(data) > 0:
        file.write("\n\n")
        file.write(f"{datetime.datetime.now()}\n[BEGINNING OF THE SESSION]\n")
    else:
        file.write(f"{datetime.datetime.now()}\n[BEGINNING OF THE SESSION]\n")
    # Closing the file
    file.close()

# Ending the backup by writing down an End of the Session sign
def endBackup():
    # Open the file in append mode only, doesn't need to read it
    file = open('Message.txt', 'a')
    file.write("[END OF THE SESSION]\n")
    file.close()

# Add a message at the end of the file
def addMessage(message):
    file = open('Message.txt', 'a')
    file.write(message + '\n')
    file.close()

# Open the file in write mode : overwrite the file
# so if it's closed right after it, it clears it
def clearBackup():
    open('Message.txt', 'w').close()
    # Starting a new backup log file
    startBackup()

# Launch the backup
def start():
    # send to the server that the backup is on
    backup.send('Backup'.encode(FORMAT))
    enabled = True
    # Initialize the backup session
    startBackup()
    while enabled:
        try:
            # receiving the message from the server
            message = backup.recv(1024).decode(FORMAT)
            # if the server is being downed
            if message.__contains__("Downing the server!"):
                endBackup()
                enabled = False
            # if an admin asked to clear the backup
            elif message.lower() == "!clearbackup":
                clearBackup()
            # if the message a message in the chat, write it in the Message.txt file
            elif message != 'Name' and ~message.__contains__('has joined the chat!'):
                addMessage(message)

        except:
            # Error gestion
            print("Error!")
            backup.close()
            break

# Start the backup
start()
# End the script
os._exit(0)
