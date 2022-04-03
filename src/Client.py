###################################################################
# Mikail YILMAZ, Ouassim MEFTAH, Hilmi CELAYIR & Quentin BERTRAND #
###################################################################
from Imports import *


ADDRESS = (SERVER, PORT)

# Creating a new client and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# Sounds used in commands
wizz_sound = AudioSegment.from_mp3("wizz_sound.mp3")
avada_kedavra = AudioSegment.from_mp3("Avada_Kedavra.mp3")

# Plays the wizz sound
def wizz():
    play(wizz_sound)

# Plays the Avada Kedavra sound
def avadaKedavra():
    play(avada_kedavra)

# Checks if command is in the commandList (from Imports.py)
def isCommand(command):
    for c in commandList:
        if c == command:
            return True
    return False


# Create a GUI class for the chat and the interface
class GUI:

    # Constructor
    def __init__(self):

        # Chat window, not visible for the moment
        self.Window = Tk()
        self.Window.withdraw()

        # Create a login window
        self.login = Toplevel()
        # Title and settings of the login window
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        # Creation of a label
        self.pls = Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        # Creation of a label
        self.labelName = Label(self.login, text="Name : ", font="Helvetica 12")

        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # Creation of an entry box for the message
        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        # Focus of the cursor
        self.entryName.focus()
        # Button
        self.continueButton = Button(self.login, text="Continue", font="Helvetica 14 bold",
                                     command=lambda: self.password(self.entryName.get()))
        self.continueButton.place(relx=0.4, rely=0.55)

        self.Window.mainloop()

    def password(self, name):
        if name.lower().__contains__("admin"):
            self.login.destroy()
            # Create a password window
            self.login = Toplevel()
            # Title and settings of the login window
            self.login.title("Login")
            self.login.resizable(width=False, height=False)
            self.login.configure(width=400, height=300)

            # Creation of a label
            self.pls = Label(self.login, text="Please enter a password\nto login as Admin", justify=CENTER,
                             font="Helvetica 14 bold")
            self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

            # Creation of a label
            self.labelPassword = Label(self.login, text="Password : ", font="Helvetica 12")

            self.labelPassword.place(relheight=0.2, relx=0.1, rely=0.2)

            # Creation a entry box for the message
            self.entryPassword = Entry(self.login, font="Helvetica 14")
            self.entryPassword.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
            # Focus of the cursor
            self.entryPassword.focus()
            # Continue button
            self.continueButton = Button(self.login, text="Continue", font="Helvetica 14 bold",
                                         command=lambda: self.continueButtonFct(name, self.entryPassword.get()))
            self.continueButton.place(relx=0.4, rely=0.55)
        else:
            self.continueButtonFct(name, None)

    def continueButtonFct(self, name, password):
        self.login.destroy()
        self.layout(name, password)

        # Thread ro receive message
        receive = threading.Thread(target=self.receive)
        receive.start()

    # Layout of the chat
    def layout(self, name, password):
        self.name = name
        self.password = password

        # Set Chat Window settings
        self.Window.deiconify()
        self.Window.title("ChatRoomServerProject")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, background="#17202A")

        self.labelHead = Label(self.Window, background="#17202A", foreground="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, background="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(self.Window, width=20, height=2, background="#17202A", foreground="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, background="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        # Inserbackground -> cursor color
        self.entryMessage = Entry(self.labelBottom, background="#2C3E50", foreground="#EAECEE", font="Helvetica 13", insertbackground='white')
        # Place the given widget
        # into the gui window
        self.entryMessage.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMessage.focus()

        # Create a Send Button
        self.buttonMessage = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, background="#ABB2B9", command=lambda: self.sendButton(self.entryMessage.get()))
        self.buttonMessage.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")
        # Create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        # Place the scroll bar into the gui window
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # Starts the thread for sending messages
    def sendButton(self, message):
        self.textCons.config(state=DISABLED)
        # Emoji.demojize turn the emoji into letters :   :heart:
        self.message = emoji.demojize(message, language='alias')
        self.entryMessage.delete(0, END)
        send = threading.Thread(target=self.sendMessage)
        send.start()

    # Recieve messages
    def receive(self):
        while True:
            try:
                # Decoding the recieved message
                message = client.recv(1024).decode(FORMAT)
                # Sending the name requested by the server
                if message == "Name":
                    client.send(self.name.encode(FORMAT))
                # Sending the password requested by the server if admin
                elif message == "Password":
                    client.send(self.password.encode(FORMAT))
                # If the password is wrong, close the window and disconnect the client
                elif message == "[NOPE]":
                    print("Wong Password!")
                    self.Window.destroy()
                # If the server has been down
                elif message.__contains__("Downing the server!"):
                    # Insert message to text box
                    self.textCons.config(state=NORMAL) # making the textCons editable
                    # Add at the end the message
                    self.textCons.insert(END, message + "\n\nDeconnection in 2 seconds!")
                    # Making the textCons uneditable
                    self.textCons.config(state=DISABLED)
                    # Make visible the message
                    self.textCons.see(END)
                    time.sleep(2) # To avoid errors
                    # Close the window
                    self.Window.destroy()
                # Playing the wizz sound
                elif message == "wizz":
                    wizz()
                # Didn't find a way to make it work
                # elif message.lower() == "[EMOTE LIST]":
                #     self.textCons.config(state=NORMAL)
                #     self.textCons.insert(END, f'{message}\nhttps://www.webfx.com/tools/emoji-cheat-sheet/')
                #     self.textCons.config(state=DISABLED)
                #     self.textCons.see(END)
                # Printing a DM with a background color to make it more eye catching
                elif message.startswith("[DM]"):
                    self.textCons.config(state=NORMAL)
                    # "mp" is like and id in html, to config it
                    self.textCons.insert(END, emoji.emojize(message, language='alias'), "mp")
                    # Config the color of the background of the message
                    self.textCons.tag_config("mp", background='#4e4e5b')
                    # Otherwise would be in color too -> avoiding huge empty space with colored background
                    self.textCons.insert(END, "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                # If kicked, send the message so the client
                # can be removed for the dictionary
                elif message == "[KICKED]":
                    time.sleep(1)
                    client.send(message.encode(FORMAT))
                    time.sleep(1)
                    self.Window.destroy()
                # Print the message kicking all the simples users
                # and plays the avada kedavra sound
                elif message.__contains__("AVADA KEDAVRA"):
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, f"{message}\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    avadaKedavra()
                # Printing a message
                else:
                    # Insert message to text box
                    self.textCons.config(state=NORMAL)
                    # emojize turn :heart: into the emoji
                    self.textCons.insert(END, emoji.emojize(message, language='alias') + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # Error gestion
                print("Error!")
                client.close()
                break

    # To send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            # If the client wants to leave the chat
            if self.message.lower() == "!quit":
                client.send(self.message.encode(FORMAT))
                time.sleep(1)
                self.Window.destroy()
            # If the client want to use a command
            elif self.message.startswith("!"):
                command = self.message.split()
                if isCommand(command[0]):
                    client.send(self.message.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, "[UNREGISTERED COMMAND]\n!help to see all the commands" + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                break
            # If the client wants to dm another client
            elif self.message.startswith("@"):
                client.send(self.message.encode(FORMAT))
                break
            # If the client wants to dm anonymously another client
            elif self.message.startswith("a@"):
                client.send(self.message.encode(FORMAT))
                break
            # If message isn't empy, send it
            elif self.message != "":
                message = f"{self.name}: {self.message}"
                client.send(message.encode(FORMAT))
                break
            # To avoid sending empty messages
            else:
                # Insert message to text box
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, "[EMPTY MESSAGE]" + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                break


# Create a GUI object
g = GUI()
# End the scrip
os._exit(0)
