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
from subprocess import call
import threading
import pyautogui
from pynput import *
from pynput.mouse import Button, Controller


'''
data stored:
plschangeme
username
hash
wifiname
runtime
gpu
cpu
memory usage
cpu usage
recalloff
False
'''

# Generate something random (I plastered a bunch of stuff together praying its random)
def Mixer():
    # input: None
    # output: SHA-512 hash
    # purpose: Generate a random SHA-512 hash using various system parameters for randomness
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
    # input: None
    # output: SHA-512 hash
    # purpose: Generate a QR code from a random SHA-512 hash and save it as an image
    hash = Mixer()
    QRCode = segno.make(hash)
    QRCode.save('qrCODE.png')
    photo = Image.open('qrCODE.png')
    resized_photo = photo.resize((300, 300))
    resized_photo.save('qrCODE.png')
    change_data(3,hash)
    return hash

def get_size(bytes, suffix="B"):
    # input: number of bytes, suffix (default "B")
    # output: readable string representation of size
    # purpose: Convert bytes into a human-readable format
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def ComputerStats():
    # input: None
    # output: Device IP, Device Name, WiFi Name, CPU, Used Memory, Total Memory, GPU
    # purpose: Retrieve and store computer stats
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
    # input: None
    # output: None
    # purpose: Update and display system stats periodically
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
    label_runtime.configure(text=f"Runtime: {int(hours):02}:{int(minutes):02}:{seconds:.02f}")
    change_data(5,"{:02}:{:02}:{:.02f}".format(int(hours), int(minutes), seconds)) #is this gonna fry my pc???
    # Schedule the next update
    APP.after(500, Update_Stats)  # Update every .5 second

def Change_Password():
    # input: None
    # output: None
    # purpose: Change the password and update the display
    newPassword = Entry_Password.get()
    change_data(1,newPassword)
    label_password.configure(text=f"Password: {newPassword}")
    
def Refresh_Hash():
    hash  = QRCodeMaker()
    label_hash.configure(text=hash[0:45])
    QR_LABEL.configure(image=PhotoImage(file='qrCODE.png'))
    

def Copy_Hash():
    # input: None
    # output: None
    # purpose: Copy the hash to clipboard
    pyperclip.copy(hash)
    
def change_data(line, text):
    # input: line number, text
    # output: None
    # purpose: Change specific line in data file
    if not isinstance(text, str):
        text = str(text)
    
    lines = open('data.txt', 'r').readlines()
    lines[line - 1] = text + '\n'
    
    with open('data.txt', 'w') as out:
        out.writelines(lines) 
    
# kinda ironic, that im getting the code for something similar to the recall system from a video that teaches how to make malware? (the youtuber does like security stuff)
def recall_system(): # im so funny with naming
    # input: None
    # output: None
    # purpose: Capture and save screenshots periodically
    global after_id
    Screenshot = pyautogui.screenshot()
    Screenshot.save("Screenshot.png")
    APP.after(1900, recall_system)  #take a screenshot every 1.9 seconds
    
def recall_toggle():
    # input: None
    # output: None
    # purpose: Toggle screenshot capturing
    global after_id
    if switch_recall.get() == 1:
        change_data(10, "recallon")
        if after_id is None: 
            recall_system()
    else:
        change_data(10, "recalloff")
        if after_id is not None:
            APP.after_cancel(after_id) 
            after_id = None

# Macro Recorder
last_input_time = None

def keyboard_inputs(key, filenumber):
    # input: key, filenumber
    # output: None
    # purpose: Record keyboard inputs
    print_time_since_last_input(filenumber)
    with open(f"macros/macro{filenumber}.txt", 'a') as file:
        file.write(f'pressed {key}\n')

def mouse_move(x, y, filenumber):
    # input: x, y, filenumber
    # output: None
    # purpose: Record mouse movements
    print_time_since_last_input(filenumber)
    with open(f"macros/macro{filenumber}.txt", 'a') as file:
        file.write(f'moved {x} {y}\n')

def mouse_scroll(x, y, sx, sy, filenumber):
    # input: x, y, scroll x, scroll y, filenumber
    # output: None
    # purpose: Record mouse scrolls
    print_time_since_last_input(filenumber)
    with open(f"macros/macro{filenumber}.txt", 'a') as file:
        file.write(f'scrolled {x} {y} {sx} {sy}\n')

def mouse_click(x, y, is_pressed, button, filenumber):
    # input: x, y, is_pressed, button, filenumber
    # output: None
    # purpose: Record mouse clicks
    print_time_since_last_input(filenumber)
    with open(f"macros/macro{filenumber}.txt", 'a') as file:
        file.write(f'click {"pressed" if is_pressed else "released"} {button} {x} {y}\n')
        
def print_time_since_last_input(filenumber):
    # input: filenumber
    # output: None
    # purpose: Log time since last input
    global last_input_time
    current_time = time.time()
    if last_input_time is not None:
        time_since_last_input = round(current_time - last_input_time, 2)
    else:
        time_since_last_input = 0
    if time_since_last_input != 0.0:
        with open(f"macros/macro{filenumber}.txt", 'a') as file:
            file.write(f'break {time_since_last_input}\n')
    last_input_time = current_time
    
# Macro stuff
macro_check = False    
keyboard_listener = None
mouse_listener = None

def macro_recorder(number):
    #input: macro number
    #output: None
    #purpose: Start or stop macro recording
    
    global macro_check, keyboard_listener, mouse_listener, last_input_time

    def start_listeners():
        global keyboard_listener, mouse_listener
        
        keyboard_listener = keyboard.Listener(on_press=lambda key: keyboard_inputs(key, number))
        mouse_listener = mouse.Listener(on_move=lambda x, y: mouse_move(x, y, number),on_scroll=lambda x, y, dx, dy: mouse_scroll(x, y, dx, dy, number),on_click=lambda x, y, button, pressed: mouse_click(x, y, button, pressed, number))
        keyboard_listener.start()
        mouse_listener.start()

    def stop_listeners():
        global keyboard_listener, mouse_listener, last_input_time
        if keyboard_listener is not None:
            keyboard_listener.stop()
            keyboard_listener = None
        if mouse_listener is not None:
            mouse_listener.stop()
            mouse_listener = None
        last_input_time = None

    if macro_check:
        stop_listeners()
        label2_macro.configure(text="Macro is not recording...", text_color="red")
        with open(f"macros/macro{number}.txt", 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            file.writelines(lines[:-3])
        macro_check = False
    else:
        open(f'macros/macro{number}.txt', 'w').close()
        label2_macro.configure(text="Macro is recording...", text_color="green")
        start_listeners()
        macro_check = True
        
# Macro reader
with open('data.txt', 'r') as file: 
    line = file.readlines()
    read_instructions_control  = line[10].strip()

def read_instructions(number):
    #input: macro number
    #output: None
    #purpose: Read and execute macro instructions
    global read_instructions_control
    with open(f'macros/macro{number}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            if parts[0] == "break":
                time.sleep(float(parts[1])) 
            elif parts[0] == "click":
                if parts[1] == "True":
                    pyautogui.mouseDown(button=parts[2], x=int(parts[3]), y=int(parts[4]))
                else:
                    pyautogui.mouseUp(button=parts[2], x=int(parts[3]), y=int(parts[4]))
            elif parts[0] == "scrolled":
                if int(parts[3]) != 0:
                    pyautogui.scroll(int(parts[3]), x=int(parts[1]), y=int(parts[2]))
                else:
                    pyautogui.scroll(int(parts[4]), x=int(parts[1]), y=int(parts[2]))
            elif parts[0] == "moved":
                pyautogui.moveTo(int(parts[1]), int(parts[2]))
            elif parts[0] == "pressed":
                pyautogui.press(parts[1])
            else:
                break  
        if read_instructions_control:
            read_instructions(number)


# Set default appearances
if __name__ == "__main__":
    start_time = time.time()

    # Flask
    def start_API():
        call(["python", "flaskAPI.py"])
        
    data = open("data.txt", "r")  # bro please in the future optimize this holy moly why have u never realized 
    password = data.readline()

    after_id = None


    # Macro Recorder
    last_input_time = None

    # Macro reader
    with open('data.txt', 'r') as file: 
        line = file.readlines()
        read_instructions_control  = line[10].strip()

    APP = CTk()
    set_appearance_mode("Dark")
    APP.geometry("1000x700")
    APP.resizable(False, False)

    recallToggle = IntVar()
    recallToggle.set(0)
    with open('data.txt', 'r') as data:
        lines = data.readlines()
        if lines[9].strip() == "recallon":
            recallToggle.set(1)

    DeviceIP, DeviceName, WifiName, CPU, UsedMemory, TotalMemory, GPU = ComputerStats()

    # Below is the QR Code

    QRFRAME = CTkFrame(master=APP, fg_color="white", border_color="gray", border_width=1, width=325, height=325)
    QRFRAME.place(x=655, y=390)  
    hash = QRCodeMaker()
    QRCODEImage = CTkImage(light_image=Image.open("qrCODE.png"),dark_image=Image.open("qrCODE.png"),size=(300, 300))
    Phrase_Label = CTkLabel(master=APP, text="HASH", font=("Arial", 30, "bold"))
    Phrase_Label.place(x=763,y=350)
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

    switch_recall = CTkSwitch(master=APP, text="Toggle Recall on or off.", command= recall_toggle,variable=recallToggle)
    switch_recall.place(rely=0.51, relx=0.01, anchor="nw")


    switch_recall = CTkSwitch(master=APP, text="Toggle Recall on or off.", command= recall_toggle,variable=recallToggle)
    switch_recall.place(rely=0.51, relx=0.01, anchor="nw")

    # Below is Macro

    label_macro = CTkLabel(master=APP,text="MACROS", font=("Arial", 30, "bold"))
    label_macro.place(rely=0.04, relx=0.83, anchor="ne")

    button_macro1 = CTkButton(master=APP, text="MACRO 1", command=lambda: macro_recorder(1), width=125, height=50)
    button_macro1.place(rely=0.1, relx=0.75, anchor="ne")


    button_macro2 = CTkButton(master=APP, text="MACRO 2", command=lambda: macro_recorder(2), width=125, height=50)
    button_macro2.place(rely=0.2, relx=0.75, anchor="ne")


    button_macro3 = CTkButton(master=APP, text="MACRO 3", command=lambda: macro_recorder(3), width=125, height=50)
    button_macro3.place(rely=0.1, relx=.9, anchor="ne")


    button_macro4 = CTkButton(master=APP, text="MACRO 4", command=lambda: macro_recorder(4), width=125, height=50)
    button_macro4.place(rely=0.2, relx=.9, anchor="ne")

    label2_macro = CTkLabel(master=APP,text="Macro is not recording...", font=("Arial", 16), text_color="red")
    label2_macro.place(rely=0.28, relx=0.79, anchor="ne")



    # Dynamic labels for CPU and memory usage
    label_memory_usage = CTkLabel(master=STATSFRAME, text=f"Memory Usage: {UsedMemory}/{TotalMemory}", font=("Arial", 30), text_color = "black")
    label_memory_usage.place(rely=0.5, relx=0.01, anchor="nw")

    label_cpu_usage = CTkLabel(master=STATSFRAME, text="CPU Usage: 0%", font=("Arial", 30), text_color="black")
    label_cpu_usage.place(rely=0.7, relx=0.01, anchor="nw")

    # I want to cry

    APP.after(500, Update_Stats)  # Start the update loop

            
    # Start Flask API in a new thread
    api_thread = threading.Thread(target=start_API)
    api_thread.daemon = True
    api_thread.start()

    # Start Tkinter main loop in the main thread
    APP.mainloop()
