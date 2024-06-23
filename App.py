from customtkinter import *
import time
import psutil
import platform
import GPUtil # remove this faulty library :C
import socket
import subprocess
import cpuinfo
from win32pdh import PDH_FMT_DOUBLE
from win32pdh import OpenQuery, CloseQuery, AddCounter
from win32pdh import CollectQueryData, GetFormattedCounterValue
from torch import *



def get_freq():
    # THANK u/RyanDy7 FOR THIS :PRAY:
    ncores = 16
    paths = []
    counter_handles = []
    query_handle = OpenQuery()
    for i in range(ncores):
        paths.append("\\Processor Information(0,{:d})\\% Processor Performance".format(i))
        counter_handles.append(AddCounter(query_handle, paths[i]))
    CollectQueryData(query_handle)
    time.sleep(1)
    CollectQueryData(query_handle)
    freq = []
    for i in range(ncores):
        (counter_type, value) = GetFormattedCounterValue(counter_handles[i], PDH_FMT_DOUBLE)
        freq.append(value*2.496/100)
    # print("{:.3f} Ghz".format(max(freq)))
    CloseQuery(query_handle)
    return "{:.3f} GHz".format(max(freq))

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
    CPUFreq = get_freq()
    CPUPercentage = psutil.cpu_percent()

    DeviceMemory = psutil.virtual_memory()
    UsedMemory = get_size(DeviceMemory.used)
    TotalMemory = get_size(DeviceMemory.total)
    
    # top works

    gpus = GPUtil.getGPUs()
    if gpus:
        GPU = torch.cuda.get_device_name()
        GPUMemTotal = get_size(gpus[0].memoryTotal * 1024 * 1024)
        GPUMemUsed = get_size(gpus[0].memoryUsed * 1024 * 1024)
        GPULoad = f"{gpus[0].load * 100:.2f}%"
        GPUTemp = f"{gpus[0].temperature} °C"
    else:
        GPU = "No GPU detected"
        GPUMemTotal = GPUMemoryUsed = GPULoad = GPUTemp = "N/A"

    return DeviceIP, DeviceName, WifiName, CPU, CPUFreq, CPUPercentage, UsedMemory, TotalMemory, GPU, GPUMemTotal, GPUMemUsed, GPULoad, GPUTemp

# Set default appearances
APP = CTk()
set_appearance_mode("Dark")
APP.geometry("1000x700")
APP.resizable(False, False)

DeviceIP, DeviceName, WifiName, CPU, CPUFreq, CPUPercentage, UsedMemory, TotalMemory, GPU, GPUMemTotal, GPUMemUsed, GPULoad, GPUTemp = ComputerStats()

# Main labels
from customtkinter import CTkLabel

label = CTkLabel(master=APP, text="COMMANDER", font=("Arial", 20))
label.place(anchor="nw")

label1 = CTkLabel(master=APP, text=f"Username: {DeviceName}", font=("Arial", 20))
label1.place(rely=0.05, anchor="nw")

label2 = CTkLabel(master=APP, text=f"Device IP: {DeviceIP}", font=("Arial", 20))
label2.place(rely=0.1, anchor="nw")

label3 = CTkLabel(master=APP, text=f"Wifi Name: {WifiName}", font=("Arial", 20))
label3.place(rely=0.15, anchor="nw")

label4 = CTkLabel(master=APP, text=f"CPU: {CPU}", font=("Arial", 20))
label4.place(rely=0.2, anchor="nw")

label5 = CTkLabel(master=APP, text=f"CPU Frequency: {CPUFreq}", font=("Arial", 20))
label5.place(rely=0.25, anchor="nw")

label6 = CTkLabel(master=APP, text=f"CPU Usage: {CPUPercentage}%", font=("Arial", 20))
label6.place(rely=0.3, anchor="nw")

label7 = CTkLabel(master=APP, text=f"Used Memory: {UsedMemory}", font=("Arial", 20))
label7.place(rely=0.35, anchor="nw")

label8 = CTkLabel(master=APP, text=f"Total Memory: {TotalMemory}", font=("Arial", 20))
label8.place(rely=0.4, anchor="nw")

label9 = CTkLabel(master=APP, text=f"GPU: {GPU}", font=("Arial", 20))
label9.place(rely=0.45, anchor="nw")

label10 = CTkLabel(master=APP, text=f"GPU Memory Total: {GPUMemTotal}", font=("Arial", 20))
label10.place(rely=0.5, anchor="nw")

label11 = CTkLabel(master=APP, text=f"GPU Memory Used: {GPUMemUsed}", font=("Arial", 20))
label11.place(rely=0.55, anchor="nw")

label12 = CTkLabel(master=APP, text=f"GPU Load: {GPULoad}", font=("Arial", 20))
label12.place(rely=0.6, anchor="nw")

label13 = CTkLabel(master=APP, text=f"GPU Temperature: {GPUTemp}", font=("Arial", 20))
label13.place(rely=0.65, anchor="nw")

APP.mainloop()
