import os
from shutil import which
import configparser

app_name = 'MusicDownloader'
video_lister = 'VideoLister'

config = configparser.ConfigParser()
config.read('config.ini')

# Specify yt-dlp location here if it's not added to the PATH
YT_DLP_LOCATION = 'yt-dlp'
if which(YT_DLP_LOCATION) is None:
    YT_DLP_LOCATION = config[app_name]['yt_dlp_path']

ids = open(config[video_lister]['list_path']).read().splitlines()
for i, link in enumerate(ids, 1):
    print(f"{len(ids)}/{i} ({i/len(ids)*100:.2f}%)")
    cmd = f"{YT_DLP_LOCATION} -o \"{config[app_name]['download_path']}/{config[app_name]['title_format']}\" {config[app_name]['yt_dl_options']} https://www.youtube.com/watch?v={link}"
    os.system(cmd)