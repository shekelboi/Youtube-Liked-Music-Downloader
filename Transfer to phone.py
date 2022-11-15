# Using ADB
import configparser
import os
from shutil import which

app_name = 'MusicUploader'

config = configparser.ConfigParser()
config.read('config.ini')

# Specify adb location here if it's not added to the PATH
ADB_LOCATION = "adb"
if which("adb") is None:
    ADB_LOCATION = config[app_name]['adb_path']

MUSIC_FOLDER = '"/storage/1F18-0B63/Music/Youtube Music"'

os.system(f"{ADB_LOCATION} push ")