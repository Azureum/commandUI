from flask import Flask, request, jsonify

# running flask server
server = Flask(__name__)

@server.route("/get-data/verification")
def get_data(verification):
    data = {
        "user": "yap"
    }

    if verification == "something":
        return jsonify(data), 200
    else:
        return 403

if  __name__ == "__main__":
    server.run(debug=True)
