from Imports import *

subprocess.run("python3 Server.py & python3 BackupMessage.py", shell=True)

os._exit(0)
