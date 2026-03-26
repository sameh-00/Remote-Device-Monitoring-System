import tkinter as tk
from ftplib import FTP
import os
from tkinter import messagebox

# إعدادات FTP
FTP_HOST = "-----"
FTP_USER = "-----"
FTP_PASS = "a3jTAGUc"
FTP_BASE_PATH = "/htdocs/F-society/"

# مجلد التحميل المحلي
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Device_Images")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# تحميل كل الصور من مجلد جهاز معين

def download_images_from_device(device_folder):
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_BASE_PATH + device_folder)

        filenames = ftp.nlst()
        for filename in filenames:
            if filename in ['.', '..']:
                continue  # تجاهل الإدخالات الخاصة
            local_path = os.path.join(DOWNLOAD_DIR, f"{device_folder}_{filename}")
            try:
                with open(local_path, 'wb') as f:
                    ftp.retrbinary(f"RETR {filename}", f.write)
            except Exception as e:
                print(f"تخطي {filename}: {e}")

        ftp.quit()
        messagebox.showinfo("نجاح", f"تم تحميل صور {device_folder} إلى {DOWNLOAD_DIR}")
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل التحميل من {device_folder}: {str(e)}")

# جلب أسماء المجلدات (أسماء الأجهزة)
def get_device_folders():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_BASE_PATH)
        folders = ftp.nlst()
        ftp.quit()
        return [f for f in folders if f not in ['.', '..']]
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل الاتصال بـ FTP: {str(e)}")
        return []

# إنشاء واجهة GUI
root = tk.Tk()
root.title("FTP Device Image Downloader")
root.geometry("500x500")
root.configure(bg='#e8f5e9')

header = tk.Label(root, text="اختر جهاز لتحميل صوره", font=("Segoe UI", 16, "bold"), bg='#e8f5e9', fg='#1b5e20')
header.pack(pady=15)

frame_list = tk.Frame(root, bg='#ffffff')
frame_list.pack(pady=10, fill="both", expand=True)

def populate_device_list():
    for widget in frame_list.winfo_children():
        widget.destroy()

    folders = get_device_folders()
    for i, folder in enumerate(folders):
        tk.Label(frame_list, text=folder, font=("Segoe UI", 11), bg='#ffffff').grid(row=i, column=0, padx=10, pady=5, sticky="w")
        tk.Button(frame_list, text="تحميل الصور", bg='#2e7d32', fg='white', 
                  command=lambda f=folder: download_images_from_device(f)).grid(row=i, column=1, padx=10, pady=5)

populate_device_list()
root.mainloop()