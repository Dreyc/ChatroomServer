###################################################################
# Mikail YILMAZ, Ouassim MEFTAH, Hilmi CELAYIR & Quentin BERTRAND #
###################################################################
import socket
import threading
import os
import time
import datetime
from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
import emoji

# Constants
# Port above 1024 (no root access needed)
PORT = 6665
# Format to encode all the messages
FORMAT = "utf-8"
# Address where the clients and the server are connected to
SERVER = 'localhost' #"10.3.141.1"
ADDRESS = (SERVER, PORT)
# Password for the admin clients
PASSWORD = "admin"

# List of all command
commandList = ["!clearbackup", "!help", "!kick",
                "!kickall", "!nbconnections", "!quit",
                "!serveroff", "!users", "!wizz"]

# List of the normal user command
commandListUser = ["!help", "!nbconnections", "!quit", "!users", "!wizz"]
