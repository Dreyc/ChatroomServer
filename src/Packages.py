import subprocess

packageList = ["tk", "pydub", "audiosegment", "emoji"]

for p in packageList:
	subprocess.run(f"pip3 install {p}", shell=True) 
