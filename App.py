# Imports
from customtkinter import *
import time
import psutil
import platform
import GPUtil
import socket

# Start timer
time.time()


# User Data (!!!)
DeviceINFO = platform.uname()
DeviceGPU = GPUtil.getGPUs()
DeviceCPU = platform.processor()
DeviceMemory = psutil.virtual_memory()

DeviceIP = socket.gethostbyname(socket.gethostname())
DeviceName = socket.gethostname()

# Set default appearances
APP = CTk()
set_appearance_mode("Dark")
APP.geometry("1000x700")
APP.resizable(None, None)

#Main stuff
label = CTkLabel(master=APP, text=DeviceName,font=("Arial" , 20))
label.place(anchor="nw")
label1 = CTkLabel(master=APP, text=DeviceIP,font=("Arial" , 20))
label1.place(rely=0.03, anchor="nw")


APP.mainloop()