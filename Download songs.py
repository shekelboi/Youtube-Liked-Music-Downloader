import os

# Specify YT-DLP location here
YT_DLP_LOCATION = "D:\Programs\yt-dlp\yt-dlp.exe"

for link in open('list.txt').read().splitlines():
    os.system(f"{YT_DLP_LOCATION} -o \"Downloaded songs/%(title)s - %(channel)s.%(ext)s\" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 {link}")