from customtkinter import *
import time
import psutil
import platform
import GPUtil
import socket
import subprocess

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
    try:
        WifiName = str(subprocess.check_output(['iwgetid -r'], shell=True)).split('\'')[1][:-2]
    except Exception as e:
        WifiName = "N/A"

    cpufreq = psutil.cpu_freq()
    CPU = platform.processor()
    CPUFreq = cpufreq.current if cpufreq else "N/A"
    CPUPercentage = psutil.cpu_percent()

    DeviceMemory = psutil.virtual_memory()
    UsedMemory = get_size(DeviceMemory.used)
    TotalMemory = get_size(DeviceMemory.total)

    gpus = GPUtil.getGPUs()
    if gpus:
        GPU = gpus[0].name
        GPUMemTotal = get_size(gpus[0].memoryTotal * 1024 * 1024)
        GPUMemoryUsed = get_size(gpus[0].memoryUsed * 1024 * 1024)
        GPULoad = f"{gpus[0].load * 100:.2f}%"
        GPUTemp = f"{gpus[0].temperature} °C"
    else:
        GPU = "No GPU detected"
        GPUMemTotal = GPUMemoryUsed = GPULoad = GPUTemp = "N/A"

    return DeviceIP, CPU, CPUFreq, CPUPercentage, UsedMemory, TotalMemory, GPU, GPUMemTotal, GPUMemoryUsed, GPULoad, GPUTemp

DeviceIP, CPU, CPUFreq, CPUPercentage, UsedMemory, TotalMemory, GPU, GPUMemTotal, GPUMemoryUsed, GPULoad, GPUTemp = ComputerStats()

# Set default appearances
APP = CTk()
set_appearance_mode("Dark")
APP.geometry("1000x700")
APP.resizable(False, False)

# Main labels
label = CTkLabel(master=APP, text="COMMANDER", font=("Arial", 20))
label.place(anchor="nw")

label1 = CTkLabel(master=APP, text=f"Device IP: {DeviceIP}", font=("Arial", 20))
label1.place(rely=0.05, anchor="nw")

label2 = CTkLabel(master=APP, text=f"CPU: {CPU}", font=("Arial", 20))
label2.place(rely=0.1, anchor="nw")

label3 = CTkLabel(master=APP, text=f"CPU Frequency: {CPUFreq} MHz", font=("Arial", 20))
label3.place(rely=0.15, anchor="nw")

label4 = CTkLabel(master=APP, text=f"CPU Usage: {CPUPercentage}%", font=("Arial", 20))
label4.place(rely=0.2, anchor="nw")

label5 = CTkLabel(master=APP, text=f"Used Memory: {UsedMemory}", font=("Arial", 20))
label5.place(rely=0.25, anchor="nw")

label6 = CTkLabel(master=APP, text=f"Total Memory: {TotalMemory}", font=("Arial", 20))
label6.place(rely=0.3, anchor="nw")

label7 = CTkLabel(master=APP, text=f"GPU: {GPU}", font=("Arial", 20))
label7.place(rely=0.35, anchor="nw")

label8 = CTkLabel(master=APP, text=f"GPU Memory Total: {GPUMemTotal}", font=("Arial", 20))
label8.place(rely=0.4, anchor="nw")

label9 = CTkLabel(master=APP, text=f"GPU Memory Used: {GPUMemoryUsed}", font=("Arial", 20))
label9.place(rely=0.45, anchor="nw")

label10 = CTkLabel(master=APP, text=f"GPU Load: {GPULoad}", font=("Arial", 20))
label10.place(rely=0.5, anchor="nw")

label11 = CTkLabel(master=APP, text=f"GPU Temperature: {GPUTemp}", font=("Arial", 20))
label11.place(rely=0.55, anchor="nw")

APP.mainloop()
