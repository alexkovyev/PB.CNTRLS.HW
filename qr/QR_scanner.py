import threading

import Queue
import serial


def bytearray_hex(data):
    return ' '.join(format(x, '02x') for x in data)


class QRScanner(serial.Serial, threading.Thread, Queue.Queue):
    def __init__(self, port):
        threading.Thread.__init__(self)
        serial.Serial.__init__(self)
        Queue.Queue.__init__(self)

        self.baudrate = 57600
        self.port = port

        self.open()
        packet = bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x1A, 0x60, 0xAB, 0xCD])
        self.write(packet)

        self.die = False

    def scan(self):
        self.read_all()
        header = bytearray(self.read(3))
        if [int(x) for x in header[:2]] != [04, 00]:
            self.read_all()
            return ""

        payload_size = header[2]
        if not payload_size:
            return ""

        payload = self.read(payload_size)

        self.read_all()
        return payload

    def run(self):
        while not self.die:
            r = self.scan()
            if r:
                self.put(r)

    def join(self):
        self.die = True
        threading.Thread.join(self, 2)
