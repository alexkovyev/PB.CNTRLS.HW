import threading

import Queue
import serial


class SerialBridge(serial.Serial, threading.Thread):
    def __init__(self, port, queue):
        threading.Thread.__init__(self)
        serial.Serial.__init__(self)

        self.baudrate = 9600
        self.port = port
        if port is not None:
            self.open()

        self.queue = queue
        self.send_q = Queue.Queue()

        self.die = False

    def __del__(self):
        self.close()

    def loop(self):
        if not self.send_q.empty():
            msg = self.send_q.get()
            self.write(msg + "\n")
        else:
            if self.in_waiting:
                line = self.readline().rstrip()
                if line:
                    self.queue.put(line)

    def send(self, msg):
        self.send_q.put(msg)

    def run(self):
        if self.port is not None:
            while not self.die:
                self.loop()

    def join(self):
        self.die = True
        threading.Thread.join(self)
