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
import tkinter as tk
from tkinter import PhotoImage
import pyperclip

start_time = time.time()

'''
data stored:
password
username
hash
wifiname
runtime
gpu
cpu
memory usage
cpu usage
'''


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
    hash = Mixer()
    QRCode = segno.make(hash)
    QRCode.save('qrCODE.png')
    photo = Image.open('qrCODE.png')
    resized_photo = photo.resize((300, 300))
    resized_photo.save('qrCODE.png')
    change_data(3,hash)
    return hash

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def ComputerStats():
    DeviceIP = socket.gethostbyname(socket.gethostname())
    DeviceName = socket.gethostname()
    change_data(2,DeviceName)
    WifiName = subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip().decode('utf-8')
    if not WifiName:
        WifiName = "N/A"
    change_data(4,WifiName)
    CPU = cpuinfo.get_cpu_info()['brand_raw']  
    change_data(6,CPU)
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
    change_data(7,GPU)

    return DeviceIP, DeviceName, WifiName, CPU, UsedMemory, TotalMemory, GPU

def Update_Stats():
    # Get updated CPU and memory usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    used_memory = get_size(memory.used)
    total_memory = get_size(memory.total)
    
    # Update labels with new stats
    label_memory_usage.configure(text=f"Memory Usage: {used_memory}/{total_memory}")
    change_data(8,used_memory+ '/'+total_memory)
    label_cpu_usage.configure(text=f"CPU Usage: {cpu_usage}%")
    change_data(9,str(cpu_usage))
    
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    label_runtime.configure(text=f"Runtime: {int(hours):02}:{int(minutes):02}:{seconds:.0f}")
    change_data(5,"{:02}:{:02}:{:.0f}".format(int(hours), int(minutes), seconds)) #is this gonna fry my pc???
    # Schedule the next update
    APP.after(500, Update_Stats)  # Update every .5 second

def Change_Password():
    newPassword = Entry_Password.get()
    change_data(1,newPassword)
    label_password.configure(text=f"Password: {newPassword}")
    
def Refresh_Hash():
    hash  = QRCodeMaker()
    label_hash.configure(text=hash[0:45])
    QR_LABEL.configure(image=PhotoImage(file='qrCODE.png'))
    

def Copy_Hash():
    pyperclip.copy(hash)
    
def change_data(line, text):
    lines = open('data.txt', 'r').readlines()
    lines[line - 1] = text + '\n'  
    out = open('data.txt', 'w')
    out.writelines(lines)
    out.close() # there might be an efficient way to do this, maybe close when the app close i dont have to close it everytime the function is called, think about this in the future

# Set default appearances
APP = CTk()
set_appearance_mode("Dark")
APP.geometry("1000x700")
APP.resizable(False, False)

DeviceIP, DeviceName, WifiName, CPU, UsedMemory, TotalMemory, GPU = ComputerStats()

# Below is the QR Code

QRFRAME = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1, width=325, height=325)
QRFRAME.place(x=650, y=390)  
hash = QRCodeMaker()
QRCODEImage = PhotoImage(file='qrCODE.png')
Phrase_Label = CTkLabel(master=APP, text="Hash", font=("Arial", 30, "bold"))
Phrase_Label.place(x=760,y=350)
QR_LABEL = CTkLabel(master=QRFRAME,text="",  image=QRCODEImage) #SOME WARNING OVER HERE
QR_LABEL.pack()

# Below is for the Stats Frame

STATSFRAME = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1, width=600, height=200)
STATSFRAME.pack(expand=True, anchor="sw", padx=10, pady=10)

label6 = CTkLabel(master=STATSFRAME, text=f"CPU: {CPU}", font=("Arial", 30), text_color = "black") 
label6.place(rely=0.1, relx=0.01, anchor="nw")

label7 = CTkLabel(master=STATSFRAME, text=f"GPU: {GPU}", font=("Arial", 30), text_color = "black")
label7.place(rely=0.3, relx=0.01, anchor="nw")

# Main labels

label = CTkLabel(master=APP, text="COMMANDER", font=('Helvetica', 50, 'bold'))
label.place(relx = 0.005,rely=0.005,anchor="nw")

label1 = CTkLabel(master=APP, text=f"Username: {DeviceName}", font=("Arial", 30))
label1.place(rely=0.1, relx=0.01, anchor="nw")

label2 = CTkLabel(master=APP, text=f"Device IP: {DeviceIP}", font=("Arial", 30))
label2.place(rely=0.15, relx=0.01, anchor="nw")

label_password = CTkLabel(master=APP, text=f"Password: {password}", font=("Arial", 30)) #do a click to reveal here or something
label_password.place(rely=0.2, relx=0.01, anchor="nw")

label4 = CTkLabel(master=APP, text=f"Wifi Name: {WifiName}", font=("Arial", 30))
label4.place(rely=0.25, relx=0.01, anchor="nw")

label_runtime = CTkLabel(master=APP, text=f"Runtime: loading", font=("Arial", 30))
label_runtime.place(rely=0.3, relx=0.01, anchor="nw")

Button_Password = CTkButton(master=APP, text="Change Password", command=Change_Password)
Button_Password.place(rely=0.37, relx=0.01, anchor="nw")

Entry_Password = CTkEntry(master=APP, placeholder_text="Enter new Password",width=300)
Entry_Password.place(rely=0.37, relx=0.16, anchor="nw")

label_hash = CTkLabel(master=APP, text=hash[0:45] + "...",width=1)
label_hash.place(rely=0.42, relx=0.16, anchor="nw")

copy_hash = CTkButton(master=APP, text="Copy Hash", command=Copy_Hash)
copy_hash.place(rely=0.42, relx=0.01, anchor="nw")

label_refresh_hash = CTkButton(master=APP, text="Refresh Hash", command=Refresh_Hash)
label_refresh_hash.place(rely=0.47, relx=0.01, anchor="nw")


# Dynamic labels for CPU and memory usage
label_memory_usage = CTkLabel(master=STATSFRAME, text=f"Memory Usage: {UsedMemory}/{TotalMemory}", font=("Arial", 30), text_color = "black")
label_memory_usage.place(rely=0.5, relx=0.01, anchor="nw")

label_cpu_usage = CTkLabel(master=STATSFRAME, text="CPU Usage: 0%", font=("Arial", 30), text_color="black")
label_cpu_usage.place(rely=0.7, relx=0.01, anchor="nw")




# Start updating stats
APP.after(500, Update_Stats)  # Start the update loop


APP.mainloop()

