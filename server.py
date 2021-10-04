import os
from dotenv import load_dotenv
from flask import Flask, request
from light_sensor import LightSensor

app = Flask(__name__)

ls = LightSensor("COM4")

load_dotenv(verbose=True)
ACCESS_KEY = os.getenv("KEY")


@app.route("/")
def main():
    data = {"data": "hello"}
    return data


@app.route("/light_sensor")
def light_sensor():

    key = request.args.get("key")

    if ACCESS_KEY == key:
        data = {"data": ls.light_value, "success": True}
        return data
    else:
        data = {"success": False}
        return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089)
