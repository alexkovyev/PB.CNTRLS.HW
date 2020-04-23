from QRScanner import QRScanner

scaner = QRScanner("/dev/ttyS2")
scaner.start()

try:
    while True:
        if not scaner.empty():
            print "Scaned:", scaner.get()
except KeyboardInterrupt:
    scaner.join()
