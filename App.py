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
import hashlib
import random
import segno
from PIL import Image

data = open("data.txt", "r") 
password = data.readline()

# Generate something random (I plastered a bunch of stuff together praying its random)

def Mixer():
    #NOT SURE IF THIS IS FULLY RANDOM OR IDK IMA PRAY IT IS 🙏🙏🙏
    a = random.randint(1, 100) 
    c = random.randint(1, 100)  
    m = random.randint(1, 100)  
    X0 = random.random() 

    mumboJumbo = list(str(os.urandom(10000)) + str(psutil.virtual_memory().used) + str(socket.gethostname()) + str(time.time()))
    X = [X0]
    for n in range(len(mumboJumbo)):
        X.append((a * X[n] + c) % m)
        
    # Convert numbers in X to strings and join them into one big string
    big_string = ''.join(str(x) for x in X)
    mumboJumbo = ''.join(mumboJumbo)
    BIGBIGSTRING = big_string + mumboJumbo + str(os.urandom(10000)) + str(psutil.virtual_memory().used) + str(socket.gethostname()) + str(time.time())
    byte_stream = BIGBIGSTRING.encode('utf-8')
    sha512 = hashlib.sha512()
    sha512.update(byte_stream)
    hash = sha512.hexdigest()
    
    return(hash)

def QRCodeMaker():
    photo = Image.open('qrCODE.png')
    QRCode = segno.make(Mixer())
    QRCode.save('qrCODE.png')


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


label = CTkLabel(master=APP, text="COMMANDER", font=('Helvetica', 50, 'bold'))
label.place(relx = 0.005,rely=0.005,anchor="nw")

label1 = CTkLabel(master=APP, text=f"Username: {DeviceName}", font=("Arial", 30))
label1.place(rely=0.1, relx=0.01, anchor="nw")

label2 = CTkLabel(master=APP, text=f"Device IP: {DeviceIP}", font=("Arial", 30))
label2.place(rely=0.15, relx=0.01, anchor="nw")

label2 = CTkLabel(master=APP, text=f"Password: {password}", font=("Arial", 30)) #do a click to reveal here or something
label2.place(rely=0.2, relx=0.01, anchor="nw")

label4 = CTkLabel(master=APP, text=f"Wifi Name: {WifiName}", font=("Arial", 30))
label4.place(rely=0.25, relx=0.01, anchor="nw")

# Below is for the Stats Frame

STATSFRAME = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1, width=600, height=200)
STATSFRAME.pack(expand=True, anchor="sw", padx=10, pady=10)

label5 = CTkLabel(master=STATSFRAME, text=f"CPU: {CPU}", font=("Arial", 30), text_color = "black")  # Fixed typo here
label5.place(rely=0.1, relx=0.01, anchor="nw")

label6 = CTkLabel(master=STATSFRAME, text=f"GPU: {GPU}", font=("Arial", 30), text_color = "black")
label6.place(rely=0.3, relx=0.01, anchor="nw")

# Dynamic labels for CPU and memory usage
label_memory_usage = CTkLabel(master=STATSFRAME, text=f"Memory Usage: {UsedMemory}/{TotalMemory}", font=("Arial", 30), text_color = "black")
label_memory_usage.place(rely=0.5, relx=0.01, anchor="nw")

label_cpu_usage = CTkLabel(master=STATSFRAME, text="CPU Usage: 0%", font=("Arial", 30), text_color="black")
label_cpu_usage.place(rely=0.7, relx=0.01, anchor="nw")


# Below is the QR Code

QRFRAME = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1, width=325, height=325)
QRFRAME.place(x=650, y=365)  
QRCodeMaker()
QRCODEImage = CTkImage(light_image="qrCODE.png", size=(200,200))



# Start updating stats
APP.after(1000, update_stats)  # Start the update loop

APP.mainloop()

