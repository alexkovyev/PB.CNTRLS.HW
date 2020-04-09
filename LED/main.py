import LED
import numpy

if __name__ == "__main__":
    led = LED.LED()
    mode = LED.LED_Mode(numpy.array([0, 1, 1]), 0, 255, 1, 1.5, 1, 2.5)
    led.add_mode("test", mode)
    led.set_mode("test")
    led.start()
