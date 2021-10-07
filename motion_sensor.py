import os
import threading
from datetime import datetime, timedelta
from bluetooth import *
from dotenv import load_dotenv
import requests


def makeURL(text, lang="en-US"):
    URL = "http://localhost:8010/call_google_assistant?textQuery="

    URL += text
    URL += "&lang="
    URL += lang

    return URL


URL = "https://graph-ap02-apnortheast2.api.smartthings.com:443/api/smartapps/installations/d89ff3f3-9625-47d8-b957-3bd379904e07/device/068f0c39-f87d-4614-a868-0c59e2a36269/command/on"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class MotionSensor(object):
    def __init__(self, MAC):

        self.token = os.getenv("TOKEN")

        self.value = 0
        self.last_value = 0
        self.last_time = datetime.now()

        self.socket = BluetoothSocket(RFCOMM)
        self.socket.connect((str(MAC), 1))
        print("BLUETOOTH CONNECTED")

        th = threading.Thread(target=self.receive_data)
        # th.daemon = True
        th.start()

    def receive_data(self):
        while True:

            try:
                msg = self.socket.recv(1024)[0]
                self.value = msg
                self.handle_data(self.value)
            except ValueError as ve:
                print(ve)
            except Exception as ex:
                print(ex)
                self.socket.close()
                break

    def handle_data(self, value):
        if value == 1 and self.last_value == 0:
            current_time = datetime.now()
            dt = (current_time - self.last_time).seconds
            if dt > 10.0:
                print("dt", dt)
                print("MOTION SENSOR DETEDTED!")

                res = requests.post(str(URL), auth=BearerAuth(str(self.token)))
                print(res)

                self.last_time = current_time

        self.last_value = value


if __name__ == "__main__":
    load_dotenv(verbose=True)
    bt = MotionSensor("98:D3:71:FD:9F:E0")
