from enum import Enum


class Color(Enum):
    RED = 1,
    GREEN = 2,
    BLUE = 3


class LEDMode:
    def __init__(self, colors=[], min_val=0, max_val=0, min_time=0, rise_time=0, max_time=0, decrease_time=0,
                 max_circles=0):
        self.colors = colors

        self.min_val = min_val
        self.max_val = max_val

        self.min_time = min_time
        self.rise_time = rise_time
        self.max_time = max_time
        self.decrease_time = decrease_time

        self.max_circles = max_circles

    def __str__(self):
        res = "{\n"
        res += "\tColors: [" + ", ".join([str(x) for x in self.colors]) + "]\n"
        res += "\tMinimum value: " + str(self.min_val) + "\n"
        res += "\tMaximum value: " + str(self.max_val) + "\n"
        res += "\tMinimum value time: " + str(self.min_time) + "\n"
        res += "\tRise time: " + str(self.rise_time) + "\n"
        res += "\tMaximum value time: " + str(self.max_time) + "\n"
        res += "\tDecrease value time: " + str(self.decrease_time) + "\n"
        res += "}"
        return res
