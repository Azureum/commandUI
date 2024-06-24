from flask import Flask, request, jsonify

# running flask server
server = Flask(__name__)

@server.route("/get-data/<verification>")
def get_data(verification):
    lines = open('filename.txt', 'r').readlines()
    data = {
        "wifiname": lines[3].strip(),
        "runtime": lines[4].strip(),
        "cpu": lines[5].strip(),
        "gpu": lines[6].strip(),
        "memory_usage": lines[7].strip(),
        "cpu_usage": lines[8].strip()
    }

    if verification == (lines[0].strip() + lines[1].strip() + lines[2].strip()):
        return jsonify(data), 200
    else:
        return "Forbidden", 403

if  __name__ == "__main__":
    server.run(debug=True)
