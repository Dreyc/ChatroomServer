import time

from Imports import *

# Same as server.py
# PORT = 6666
SERVER = "localhost" #"10.3.141.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Creating a new client and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# Sound of the wizz command
wizz_sound = AudioSegment.from_mp3("wizz_sound.mp3")
avada_kedavra = AudioSegment.from_mp3("Avada_Kedavra.mp3")

def wizz():
    play(wizz_sound)

def avadaKedavra():
    play(avada_kedavra)

# Open hyperlin
def openUrl(url):
    webbrowser.open_new_tab(url)


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
            self.pls = Label(self.login, text="Please enter password\nto login as Admin", justify=CENTER, font="Helvetica 14 bold")
            self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

            # Creation of a label
            self.labelPassword = Label(self.login, text="Password : ", font="Helvetica 12")

            self.labelPassword.place(relheight=0.2, relx=0.1, rely=0.2)

            # Creation a entry box for the message
            self.entryPassword = Entry(self.login, font="Helvetica 14")
            self.entryPassword.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
            # Focus of the cursor
            self.entryPassword.focus()
            #continue button
            self.continueButton = Button(self.login, text="Continue", font="Helvetica 14 bold",
                                         command=lambda: self.continueButtonFct(name, self.entryPassword.get()))
            self.continueButton.place(relx=0.4, rely=0.55)
        else:
            self.continueButtonFct(name, None)


    def continueButtonFct(self, name, password):
        self.login.destroy()
        self.layout(name, password)

        # thread ro receive message
        receive = threading.Thread(target=self.receive)
        receive.start()

    # Layout of the chat
    def layout(self, name, password):
        self.name = name
        self.password = password

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

        # Inserbackground -> cursor color
        self.entryMessage = Entry(self.labelBottom, background="#2C3E50", foreground="#EAECEE", font="Helvetica 13",
                                  insertbackground='white')

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
        self.message = emoji.demojize(message, language='alias')
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
                elif message == "Password":
                    client.send(self.password.encode(FORMAT))
                elif message == "[NOPE]":
                    print("Wong Password!")
                    self.Window.destroy()
                elif message.__contains__("Downing the server!"):
                    # insert message to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\nDeconnection in 2 seconds!")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    time.sleep(2)
                    self.Window.destroy()
                elif message == "wizz":
                    wizz()
                elif message.lower() == "[EMOTE LIST]":
                    hyperlink = HyperlinkManager(self.textCons)
                    self.textCons.config(state=NORMAL)
                    #self.textCons.insert(END, message, hyperlink.add(
                    #    partial(webbrowser.open("https://www.webfx.com/tools/emoji-cheat-sheet/"))), "mp")
                    self.textCons.insert(END, f'{message}\nhttps://www.webfx.com/tools/emoji-cheat-sheet/')
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                elif message.startswith("[DM]"):
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, emoji.emojize(message, language='alias'), "mp")
                    self.textCons.tag_config("mp", background='#4e4e5b')
                    # Otherwise would be in color too
                    self.textCons.insert(END, "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                elif message == "[KICKED]":
                    time.sleep(1)
                    client.send(message.encode(FORMAT))
                    time.sleep(1)
                    self.Window.destroy()
                elif message.__contains__("AVADA KEDAVRA"):
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, f"{message}\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    avadaKedavra()
                else:
                    # insert message to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, emoji.emojize(message, language='alias') + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                 #Error gestion
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
            elif self.message.startswith("@"):
                client.send(self.message.encode(FORMAT))
                break
            elif self.message != "":
                message = f"{self.name}: {self.message}"
                client.send(message.encode(FORMAT))
                break
            else:
                # insert message to text box
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, "[EMPTY MESSAGE]" + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                break


# Create a GUI object
g = GUI()
os._exit(0)
