from bluetooth import *
import threading
import requests
from datetime import datetime, timedelta


def makeURL(text, lang="en-US"):
    URL = "http://localhost:8010/call_google_assistant?textQuery="

    URL += text
    URL += "&lang="
    URL += lang

    return URL


class MotionSensor(object):
    def __init__(self, MAC):

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
                res = requests.get(makeURL(text="입실 가상 스위치 켜", lang="ko-KR"))
                self.last_time = current_time

        self.last_value = value


if __name__ == "__main__":
    bt = MotionSensor("98:D3:71:FD:9F:E0")
    # bt.receive_data()
