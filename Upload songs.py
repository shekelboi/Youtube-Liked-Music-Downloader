# Using ADB
import configparser
import os
from shutil import which

app_name = 'MusicUploader'

config = configparser.ConfigParser()
config.read('config.ini')

# Specify adb location here if it's not added to the PATH
ADB_LOCATION = "adb"
if which(ADB_LOCATION) is None:
    ADB_LOCATION = config[app_name]['adb_path']

cmd = f"{ADB_LOCATION} push \"{config[app_name]['source_path']}\" \"{config[app_name]['target_path']}\""
os.system(cmd)