from customtkinter import *
import time
import psutil
import platform
import GPUtil # damn nvidia monopoly
from pyadl import *
import socket
import subprocess
import cpuinfo
import threading

data = open("data.txt", "r") 
password = data.readline()
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def ComputerStats():
    DeviceINFO = platform.uname()
    DeviceIP = socket.gethostbyname(socket.gethostname())
    DeviceName = socket.gethostname()
    WifiName = subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip().decode('utf-8')
    if not WifiName:
        WifiName = "N/A"
    CPU = cpuinfo.get_cpu_info()['brand_raw']  
    DeviceMemory = psutil.virtual_memory()
    UsedMemory = get_size(DeviceMemory.used)
    TotalMemory = get_size(DeviceMemory.total)
    
    gpus = GPUtil.getGPUs()
    if gpus:
        GPU = gpus[0].name
    elif ADLManager.getInstance().getDevices():
        GPU = str(ADLManager.getInstance().getDevices()[0].adapterName).strip("b'")
    else:
        GPU = "No GPU detected"

    return DeviceIP, DeviceName, WifiName, CPU, UsedMemory, TotalMemory, GPU

def update_stats():
    # Get updated CPU and memory usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    used_memory = get_size(memory.used)
    total_memory = get_size(memory.total)
    
    # Update labels with new stats
    label_cpu_usage.configure(text=f"CPU Usage: {cpu_usage}%")
    label_memory_usage.configure(text=f"Memory Usage: {used_memory}/{total_memory}")
    # Schedule the next update
    APP.after(1000, update_stats)  # Update every 1 second

# Set default appearances
APP = CTk()
set_appearance_mode("Dark")
APP.geometry("1000x700")
APP.resizable(False, False)

DeviceIP, DeviceName, WifiName, CPU, UsedMemory, TotalMemory, GPU = ComputerStats()

# Main labels

Login_Frames = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1)
Login_Frames.pack(expand=True)

label = CTkLabel(master=Login_Frames, text="COMMANDER", font=('Helvetica', 30, 'bold'))
label.place(anchor="nw")

label1 = CTkLabel(master=Login_Frames, text=f"Username: {DeviceName}", font=("Arial", 20))
label1.place(rely=0.05, anchor="nw")

label2 = CTkLabel(master=Login_Frames, text=f"Device IP: {DeviceIP}", font=("Arial", 20))
label2.place(rely=0.1, anchor="nw")

label3 = CTkLabel(master=Login_Frames, text=f"Device IP: {DeviceIP}", font=("Arial", 20))
label3.place(rely=0.1, anchor="nw")

label4 = CTkLabel(master=Login_Frames, text=f"Wifi Name: {WifiName}", font=("Arial", 20))
label4.place(rely=0.20, anchor="nw")

lavel5 = CTkLabel(master=APP, text=f"CPU: {CPU}", font=("Arial", 20))
lavel5.place(rely=0.25, anchor="nw")

label6 = CTkLabel(master=APP, text=f"GPU: {GPU}", font=("Arial", 20))
label6.place(rely=0.3, anchor="nw")

# Dynamic labels for CPU and memory usage
label_memory_usage = CTkLabel(master=APP, text=f"Memory Usage: {UsedMemory}/{TotalMemory}", font=("Arial", 20))
label_memory_usage.place(rely=0.35, anchor="nw")

label_cpu_usage = CTkLabel(master=APP, text="CPU Usage: 0%", font=("Arial", 20))
label_cpu_usage.place(rely=0.4, anchor="nw")

# Start updating stats
APP.after(1000, update_stats)  # Start the update loop

APP.mainloop()
