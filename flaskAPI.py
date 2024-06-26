from flask import Flask, request, jsonify, send_file
import subprocess
import os
import threading
from App import change_data, read_instructions
import time
# running flask server
server = Flask(__name__)
lines = open('data.txt', 'r').readlines()

@server.route("/get-data/<verification>")
def get_data(verification):
    if verification == (lines[0].strip() + lines[1].strip() + lines[2].strip()):
        data = {
        "wifiname": lines[3].strip(),
        "runtime": lines[4].strip(),
        "cpu": lines[5].strip(),
        "gpu": lines[6].strip(),
        "memory_usage": lines[7].strip(),
        "cpu_usage": lines[8].strip()
        }

        return jsonify(data), 200
    else:
        return "Forbidden", 403
    
@server.route("/send-command/<command>/<verification>")
def send_commands(verification, command):
    if verification == (lines[0].strip() + lines[1].strip() + lines[2].strip()):
        if command == "restart":
            subprocess.call(["shutdown", "-r", "-t", "0"])
        elif command == "shutdown":
            subprocess.call(["shutdown", "-s", "-t", "0"])
        elif command == "sleep":
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            #more commands
        elif command == "wifirestart":
            os.system('nmcli radio wifi off')
            time.sleep(10)
            os.system('nmcli radio wifi on')
        return "Success", 200
    else:
        return "Forbidden", 403
    
@server.route("/get-screen/<verification>")
def get_screen(verification):
    if verification == (lines[0].strip() + lines[1].strip() + lines[2].strip()):
        return send_file('screenshot.png', mimetype='image/png')
    else:
        return "Forbidden", 403
    
@server.route("/send_macro/<number>/<loop>/<verification>")
def send_macro(verification,number,loop):
    if verification == (lines[0].strip() + lines[1].strip() + lines[2].strip()) and loop == "True" or "False":
        cd = threading.Thread(target=change_data, args= (11,loop))
        cd.start()
        cd.join()
        ri = threading.Thread(target=read_instructions, args= (number))
        ri.start()
        ri.join()
        return "Success", 200
    else:
        return "Forbidden", 403

if  __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000)
