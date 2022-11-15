import os
from shutil import which

# Specify YT-DLP location here if it's not added to the PATH
YT_DLP_LOCATION = "yt-dlp"
if which("yt-dlp") is None:
    YT_DLP_LOCATION = "D:\\Programs\\yt-dlp\\yt-dlp.exe"

ids = open('list.txt').read().splitlines()
for i, link in enumerate(ids, 1):
    print(f"{len(ids)}/{i} ({i/len(ids)*100:.2f}%)")
    os.system(f"{YT_DLP_LOCATION} -o \"Downloaded songs/%(title)s - %(channel)s.%(ext)s\" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 https://www.youtube.com/watch?v={link}")