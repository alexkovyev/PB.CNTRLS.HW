'''
import time

import serial

ser = serial.Serial()
ser.baudrate = 57600
ser.port = "/dev/ttyS2"
ser.open()


def read(n):
    received = ser.read(n)
    #return hex(int(received.encode('hex'), 16))
    return bytearray(received)


def scan():
    time.sleep(0.1)

    r = read(3)
    print ' '.join(format(x, '02x') for x in r)

    payload_size = r[2]
    print "Size of payload:", payload_size

    print "Payload:"
    r = read(payload_size)
    print ' '.join(format(x, '02x') for x in r)
    print bytes(r)

    while ser.in_waiting:
        print read(1)
    print "---"


#try:
packet = bytearray([0x7E, 0x00, 0x08, 0x01, 0x00, 0x1A, 0x60, 0xAB, 0xCD])
ser.write(packet)
while True:
    scan()
#except Exception as e:
#    print e

'''

from QR_scanner import QRScanner

scaner = QRScanner("/dev/ttyS2")
scaner.start()

try:
    while True:
        if not scaner.empty():
            print
            "Scaned:", scaner.get()
except KeyboardInterrupt:
    scaner.join()
