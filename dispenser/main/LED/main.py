import numpy

import LED

if __name__ == "__main__":
    led = LED.LED()
    mode = LED.LEDMode(numpy.array([0, 1, 1]), 0, 255, 1, 1.5, 1, 2.5)
    led.add_mode("test", mode)
    led.set_mode("test")
    led.start()
