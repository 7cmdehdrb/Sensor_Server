import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from light_sensor import LightSensor
from motion_sensor import MotionSensor

load_dotenv(verbose=True)

app = Flask(__name__)

# ls = LightSensor("/dev/ttyACM0")
ms = MotionSensor("98:D3:71:FD:9F:E0")

ACCESS_KEY = os.getenv("KEY")


@app.route("/")
def main():
    data = {"data": "HELLO WORLD!"}
    return jsonify(data)


@app.route("/light_sensor")
def light_sensor():

    key = request.args.get("key")

    if ACCESS_KEY == key:
        data = {"data": int(0), "success": True}
        return jsonify(data)
    else:
        data = {"success": False}
        return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
