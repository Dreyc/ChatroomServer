import socket
import threading
import os
import time
import datetime
from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
import emoji

# Constantes
# Port above 1024 (no root access needed)
PORT = 6665
FORMAT = "utf-8"
SERVER = 'localhost' #"10.3.141.1"
ADDRESS = (SERVER, PORT)
PASSWORD = "admin"

commandList = ["!clearbackup", "!help", "!kick",
                "!kickall", "!nbconnections", "!quit",
                "!serveroff", "!users", "!wizz"]

commandListUser = ["!help", "!nbconnections", "!quit", "!users", "!wizz"]
