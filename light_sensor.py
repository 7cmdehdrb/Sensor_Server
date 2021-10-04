import serial
import threading
from time import sleep


class LightSensor(object):
    def __init__(self, port_num):

        self.port_num = port_num
        self.light_value = 0

        self.ser = serial.Serial(
            port=port_num,
            baudrate=9600,
        )

        self.th = threading.Thread(target=self.receive_data)
        self.th.daemon = True
        self.th.start()

    def receive_data(self):
        line = []

        while True:
            try:
                data = self.ser.read()

                line.append(data)

                if len(line) >= 6:
                    if line[-2] == "\n".encode():
                        self.handleData(line)
                        del line[:]

            except Exception as ex:
                print(ex)

    def handleData(self, line):
        self.light_value = ord(line[-1])


if __name__ == "__main__":
    bt = LightSensor("COM4")

    while True:
        print(bt.light_value)
        sleep(0.1)
