import tkinter as tk
from tkinter import ttk
import pyodbc

# إعدادات الاتصال بقاعدة البيانات
DB_SERVER = '------.public.databaseasp.net'
DB_NAME = '------'
DB_USER = '------'
DB_PASSWORD = '------X54h@B'

# الاتصال بقاعدة البيانات
def connect_db():
    conn_str = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={DB_SERVER};
        DATABASE={DB_NAME};
        UID={DB_USER};
        PWD={DB_PASSWORD};
        Encrypt=yes;
        TrustServerCertificate=yes;
        MARS_Connection=yes;
    '''
    return pyodbc.connect(conn_str)

# جلب الأجهزة من قاعدة البيانات
def fetch_devices():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT device_name, Script_Status FROM user_devices")
    devices = cursor.fetchall()
    conn.close()
    return devices

# تحديث حالة الجهاز
def toggle_status(device_name, current_status):
    new_status = 'off' if current_status == 'on' else 'on'
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_devices
        SET Script_Status = ?
        WHERE device_name = ?
    """, (new_status, device_name))
    conn.commit()
    conn.close()
    refresh_table()

# تحديث الجدول بعد أي تغيير
def refresh_table():
    for widget in frame_table.winfo_children():
        widget.destroy()

    devices = fetch_devices()

    for i, (device_name, status) in enumerate(devices):
        tk.Label(frame_table, text=device_name, bg='#f0f0f0', font=("Segoe UI", 11)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        status_label = tk.Label(frame_table, text=f"Status: {status.upper()}", bg='#f0f0f0', fg='#333', font=("Segoe UI", 10, "italic"))
        status_label.grid(row=i, column=1, padx=10, pady=5)
        btn = tk.Button(frame_table, text=f"Turn {'OFF' if status == 'on' else 'ON'}", 
                        bg='#4caf50' if status == 'off' else '#f44336', fg='white', 
                        command=lambda d=device_name, s=status: toggle_status(d, s))
        btn.grid(row=i, column=2, padx=10, pady=5)

# واجهة المستخدم
root = tk.Tk()
root.title("Device Script Control")
root.geometry("500x500")
root.configure(bg="#0b0f0f")

style = ttk.Style()
style.configure("Treeview", font=("Segoe UI", 10))

header = tk.Label(root, text="Control Devices", font=("Segoe UI", 16, "bold"), bg='#e0f7fa', fg='#00796b')
header.pack(pady=15)

frame_table = tk.Frame(root, bg="#000000")
frame_table.pack(pady=10, fill="both", expand=True)

refresh_table()
root.mainloop()
