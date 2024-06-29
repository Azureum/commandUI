from flask import Flask, request, jsonify, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import subprocess
import os
import threading
import logging
from App import change_data, read_instructions
from waitress import serve
import time


logging.basicConfig(level=logging.INFO)

server = Flask(__name__)
CORS(server)
lines = open('data.txt', 'r').readlines()


limiter = Limiter(
    get_remote_address,
    app=server,
    default_limits=["3600 per hour"],
    storage_uri="memory://",
)

def verify_user(verification):
    return verification == (lines[0].strip() + lines[1].strip() + lines[2].strip())

@server.route("/<verification>", methods=['GET'])
@limiter.limit("2/minute")
def verify(verification):
    if verify_user(verification):
        return jsonify({"status": "verified"}), 200
    else:
        return jsonify({"status": "not verified"}), 401

@server.route("/get-data/<verification>")
@limiter.limit("3/second")
def get_data(verification):
    lines = open('data.txt', 'r').readlines()
    if verify_user(verification):
        data = {
            "wifiname": str(lines[3].strip()),
            "runtime": str(lines[4].strip()),
            "cpu": str(lines[5].strip()),
            "gpu": str(lines[6].strip()),
            "memory_usage": str(lines[7].strip()),
            "cpu_usage": str(lines[8].strip()),
            "recallstatus": str(lines[9].strip())
        }
        return jsonify(data), 200
    else:
        return "Forbidden", 403

@server.route("/send-command/<command>/<verification>", methods=['GET'])
@limiter.limit("1/second")
def send_commands(verification, command):
    if verify_user(verification):
        try:
            if command == "restart":
                subprocess.call(["shutdown", "-r", "-t", "0"])
            elif command == "shutdown":
                subprocess.call(["shutdown", "-s", "-t", "0"])
            elif command == "sleep":
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif command == "wifirestart":
                os.system('nmcli radio wifi off')
                time.sleep(10)
                os.system('nmcli radio wifi on')
            else:
                return jsonify({"status": "Invalid command"}), 400
            return jsonify({"status": "Success"}), 200
        except Exception as e:
            logging.error(f"Command execution failed: {e}")
            return jsonify({"status": "Error"}), 500
    else:
        return jsonify({"status": "Forbidden"}), 403

@server.route("/get-screen/<verification>", methods=['GET'])
@limiter.limit("10/second", override_defaults=True)
def get_screen(verification):
    if verify_user(verification):
        return send_file('screenshot.png', mimetype='image/png')
    else:
        return jsonify({"status": "Forbidden"}), 403

@server.route("/send_macro/<number>/<loop>/<verification>", methods=['GET'])
def send_macro(verification, number, loop):
    if verify_user(verification) and loop in ["True", "False"]:
        try:
            cd = threading.Thread(target=change_data, args=(11, loop))
            cd.start()
            cd.join()
            ri = threading.Thread(target=read_instructions, args=(number,))
            ri.start()
            ri.join()
            return jsonify({"status": "Success"}), 200
        except Exception as e:
            logging.error(f"Macro execution failed: {e}")
            return jsonify({"status": "Error"}), 500
    else:
        return jsonify({"status": "Forbidden"}), 403

if __name__ == "__main__":
    serve(server, host="", port=80)