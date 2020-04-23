ON_ORANGE_PI = False

import ctypes
import multiprocessing
import time

if ON_ORANGE_PI:
    import wiringpi

from LEDMode import *


def rescale(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class LED(object):
    """
    Class that is responsible for controlling LED strip.
    """

    def __init__(self):
        super(LED, self).__init__()

        self.modes = {}
        self.current_mode = multiprocessing.Value(ctypes.c_char_p, None)

        self.steps = 200

        self.die = False
        self.loop_process = multiprocessing.Process(target=self._run)

        self.pins = {Color.RED: 23, Color.GREEN: 22, Color.BLUE: 24}

    def wiringpi_setup(self):
        if ON_ORANGE_PI:
            wiringpi.wiringPiSetup()

            for _, pin in self.pins.items():
                wiringpi.pinMode(pin, 1)
                wiringpi.softPwmCreate(pin, 0, 100)

    def set_color(self, color, value):
        scaled_val = rescale(value, 0, 255, 0, 100)
        # print color, int(scaled_val)
        if ON_ORANGE_PI:
            wiringpi.softPwmWrite(self.pins[color], int(scaled_val))

    def set_colors(self, values):
        for color, val in zip([Color.RED, Color.GREEN, Color.BLUE], values):
            self.set_color(color, val)

    def set_all_colors(self, value):
        self.set_colors({Color.RED: value, Color.GREEN: value, Color.BLUE: value})

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def set_mode(self, name):
        if name not in self.modes:
            print "Unknown mode:", name
            return
        if self.current_mode.value != name:
            print "Current mode:", name
            self.current_mode.value = name

            try:
                self.loop_process.terminate()
            except:
                pass
            self.loop_process = multiprocessing.Process(target=self._run)
            self.loop_process.start()

    def _colors_slope(self, start_val, slope_time, colors, step):
        delay = float(slope_time) / self.steps
        val = start_val
        for i in range(self.steps):
            val += step
            self.set_colors([int(x) * val for x in colors])
            time.sleep(delay)

    def _loop(self):
        if self.current_mode.value is not None:
            mode = self.modes[self.current_mode.value]

            self.set_colors([int(x) * mode.min_val for x in mode.colors])
            time.sleep(mode.min_time)

            step = float(mode.max_val - mode.min_val) / self.steps
            self._colors_slope(mode.min_val, mode.rise_time, mode.colors, step)

            self.set_colors([int(x) * mode.max_val for x in mode.colors])
            time.sleep(mode.max_time)

            self._colors_slope(mode.max_val, mode.decrease_time, mode.colors, -step)

    def _run(self):
        if ON_ORANGE_PI:
            self.wiringpi_setup()
        circles = 0
        while not self.die:
            if self.current_mode.value is not None:
                max_circles = self.modes[self.current_mode.value].max_circles
                if max_circles != 0 and circles >= max_circles:
                    break
            self._loop()
            circles += 1

    def join(self):
        self.die = True
        self.loop_process.join()

    def start(self):
        self.loop_process.start()
