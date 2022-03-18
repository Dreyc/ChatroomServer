from Imports import *

# Same as server.py
PORT = 6666
SERVER = "localhost"  # socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Creating a new client and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# Sound of the wizz command
wizz_sound = AudioSegment.from_mp3("wizz_sound.mp3")


def wizz():
    play(wizz_sound)


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

        # Creation a entry box for the message
        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        # Focus of the cursor
        self.entryName.focus()

        # Button
        self.continueButton = Button(self.login, text="Continue", font="Helvetica 14 bold",
                                     command=lambda: self.continueButtonFct(self.entryName.get()))
        self.continueButton.place(relx=0.4, rely=0.55)
        self.Window.mainloop()

    def continueButtonFct(self, name):
        self.login.destroy()
        self.layout(name)

        # thread ro receive message
        receive = threading.Thread(target=self.receive)
        receive.start()

    # Layout of the chat
    def layout(self, name):
        self.name = name

        # Set Window settings
        self.Window.deiconify()
        self.Window.title("ChatRoomServerProject")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, background="#17202A")
        self.labelHead = Label(self.Window, background="#17202A", foreground="#EAECEE", text=self.name,
                               font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, background="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        self.textCons = Text(self.Window, width=20, height=2, background="#17202A", foreground="#EAECEE",
                             font="Helvetica 14", padx=5, pady=5)

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, background="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMessage = Entry(self.labelBottom, background="#2C3E50", foreground="#EAECEE", font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMessage.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        self.entryMessage.focus()

        # create a Send Button
        self.buttonMessage = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20,
                                    background="#ABB2B9", command=lambda: self.sendButton(self.entryMessage.get()))

        self.buttonMessage.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1, relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # def on_press(self, key):
    #     if key == keyboard.Key.enter:
    #         self.sendButton(self.entryMessage.get())
    #
    # listener = keyboard.Listener(on_press=on_press(self))
    # listener.start()

    # Starts the thread for sending messages
    def sendButton(self, message):
        self.textCons.config(state=DISABLED)
        self.message = message
        self.entryMessage.delete(0, END)
        send = threading.Thread(target=self.sendMessage)
        send.start()

    # Receeve messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == "Name":
                    client.send(self.name.encode(FORMAT))
                elif message == "Downing the server!":
                    # insert message to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\nDeconnection in 2 seconds!")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    time.sleep(2)
                    self.Window.destroy()
                elif message == "wizz":
                    wizz()
                else:
                    # insert message to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")
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
            if self.message == DISCONNECT_MESSAGE or self.message.lower() == "quit":
                client.send(DISCONNECT_MESSAGE.encode(FORMAT))
                time.sleep(1)
                self.Window.destroy()
            elif self.message.startswith("!"):
                client.send(self.message.encode(FORMAT))
                break
            else:
                message = f"{self.name}: {self.message}"
                client.send(message.encode(FORMAT))
                break


# Create a GUI object
g = GUI()
os._exit(0)
