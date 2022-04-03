import subprocess

packageList = ["tk", "pydub", "audiosegment", "emoji"]

for p in packageList:
	subprocess.run(f"pip install {p}", shell=True) 
