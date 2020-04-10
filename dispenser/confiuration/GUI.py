# coding=utf-8
import Tkinter as tk
import json
import os
import tkFileDialog
import ttk
from math import cos, sin

# You should probably change this to import dispenser_main/LED/LEDMode.py
from LEDMode import LEDMode


class Labeled_entry(tk.Frame):
    def __init__(self, parent, label, entry_var):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label, anchor="w")
        self.entry = tk.Entry(self, textvariable=entry_var)

        validate_cmd = (self.register(self.validate_input),
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry.configure(validate='key', validatecommand=validate_cmd)

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="bottom", fill="x")

    @staticmethod
    def validate_input(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if action is "0":
            return True

        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def get(self):
        return self.entry.get()


class Mode_graph(tk.Canvas):
    def __init__(self, parent, values, colors):
        tk.Canvas.__init__(self, parent)

        self.width = 300
        self.height = 300

        self.start_x = 10
        self.start_y = self.height - 20

        self.configure(width=self.width, height=self.height)

        self.values = values
        self.colors = colors

    def line(self, x, y, length, angle, color="black"):
        x2 = x + length * cos(angle)
        y2 = y + length * sin(angle)

        self.create_line(self.start_x + x, self.start_y + y,
                         self.start_x + x2, self.start_y + y2, width=2, fill=color)

    def line_points(self, x, y, x2, y2, color="black"):
        self.create_line(self.start_x + x, self.start_y + y,
                         self.start_x + x2, self.start_y + y2, width=2, fill=color)

    def draw_grid(self, px_per_sec, px_per_level, rows=True, cols=True):
        if rows:
            for x in range(0, self.width, int(px_per_sec)):
                self.create_line(x + self.start_x, 0, x + self.start_x, self.height, fill="grey")

        if cols:
            for i in range(self.height / abs(int(px_per_level)) / 25):
                y = 25 * i * abs(px_per_level)
                self.create_line(0, y, self.width, y, fill="grey")

    def draw(self):
        try:
            self.delete("all")

            values = {key: float(val.get()) if val.get() else 0 for key, val in self.values.items()}

            px_per_level = -float(self.height - (self.height - self.start_y) - 20) / 255
            px_per_sec = (self.width - self.start_x) / (
                        values["min_time"] + values["max_time"] + values["rise_time"] + values["decrease_time"])

            self.draw_grid(px_per_sec, px_per_level, True, False)

            color = '#%02x%02x%02x' % tuple([255 if x.get() else 0 for x in self.colors])

            min_y = values["min_val"] * px_per_level
            min_length = values["min_time"] / 2 * px_per_sec
            self.line(0, min_y, min_length, 0, color)

            max_x = values["rise_time"] * px_per_sec + min_length
            max_y = values["max_val"] * px_per_level
            max_length = values["max_time"] * px_per_sec
            self.line(max_x, max_y, max_length, 0, color)

            self.line_points(min_length, min_y, max_x, max_y, color)

            max_end_x = max_x + max_length
            decrease_end_x = max_x + max_length + values["decrease_time"] * px_per_sec
            self.line_points(max_end_x, max_y, decrease_end_x, min_y, color)

            self.line(decrease_end_x, min_y, values["min_time"] / 2 * px_per_sec, 0, color)
        except ZeroDivisionError:
            pass


class Mode_inputs(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.params_frame = tk.Frame(self)

        params_labels = {
            "max_circles": "Максимальное количество циклов",
            "decrease_time": "Время угасания",
            "rise_time": "Время рассвета",
            "min_val": "Минимальное значение",
            "max_val": "Максимальное значение",
            "max_time": "Время максимального значения",
            "min_time": "Время минимального значения"
        }
        self.entries = LEDMode().__dict__.keys()
        self.entries.remove("colors")
        for field in self.entries:
            s_var = tk.StringVar()
            s_var.trace("w", lambda name, index, mode: self.graph.draw())
            setattr(self, field + "_var", s_var)
            label = params_labels[field]
            entry = Labeled_entry(self.params_frame, label, getattr(self, field + "_var"))
            setattr(self, field + "_entry", entry)

        self.colors_frame = tk.Frame(self, borderwidth=2)

        self.colors_label = tk.Label(self.colors_frame, text="Colors:")
        self.colors = []
        self.colors_chkbs = []

        for label in ["Red", "Green", "Blue"]:
            b_var = tk.BooleanVar()
            b_var.trace("w", lambda name, index, mode: self.graph.draw())
            self.colors.append(b_var)
            self.colors_chkbs.append(tk.Checkbutton(self.colors_frame, text=label,
                                                    variable=self.colors[-1]))

        values = {x[:-4]: getattr(self, x) for x in self.__dict__.keys() if x.endswith("_var")}
        self.graph = Mode_graph(self, values, self.colors)

        self.place_entries()
        self.place_colors()

        self.graph.grid(column=0, row=1, pady=10)

    def place_entries(self):
        for i, field in zip(range(len(self.entries)), self.entries):
            entry = getattr(self, field + "_entry")
            entry.grid(column=0, row=i, sticky="NSEW")
        self.params_frame.grid(column=0, row=0, sticky="NSEW")

    def place_colors(self):
        for i, color_chkb in zip(range(len(self.colors_chkbs)), self.colors_chkbs):
            color_chkb.grid(column=0, row=i, sticky="W")
        self.colors_frame.grid(column=1, row=0, sticky="W")

    def get_led_mode(self):
        res = LEDMode()

        values = [x for x in self.__dict__.keys() if x.endswith("_var")]
        for value in values:
            setattr(res, value[:-4], getattr(self, value).get())

        res.colors = [x.get() for x in self.colors]

        return res

    def set_led_mode(self, mode):
        values = [x for x in self.__dict__.keys() if x.endswith("_var")]

        for value in values:
            getattr(self, value).set(getattr(mode, value[:-4]))

        for i, color in zip(range(len(self.colors)), self.colors):
            color.set(mode.colors[i])


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background='white')

        self.tabs = ttk.Notebook(self.window)

        self.strip_mode_params = Mode_inputs(self.tabs)
        # self.qr_mode_params = Mode_inputs(self.tabs)
        # self.mode_params.pack()
        self.tabs.add(self.strip_mode_params, text="лента")
        # self.tabs.add(self.qr_mode_params, text="QR")

        self.tabs.pack(expand=1, fill="both")

        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.window.mainloop()

    def save(self):
        file_path = tkFileDialog.asksaveasfilename(initialdir=os.getcwd(), title="Save",
                                                   filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if file_path:
            strip_led_mode = self.strip_mode_params.get_led_mode()
            # qr_led_mode = self.qr_mode_params.get_led_mode()
            both = {
                "strip": strip_led_mode.__dict__,
                # "qr": qr_led_mode.__dict__
            }
            with open(file_path, "w") as f:
                json.dump(both, f, indent=4)

    def load(self):
        file_path = tkFileDialog.askopenfilename(initialdir=os.getcwd(), title="Open",
                                                 filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if file_path:
            with open(file_path, "r") as f:
                j = json.load(f)
                strip_mode = LEDMode()
                strip_mode.__dict__ = j["strip"]
                # qr_mode = LEDMode()
                # qr_mode.__dict__ = j["qr"]

                self.strip_mode_params.set_led_mode(strip_mode)
                # self.qr_mode_params.set_led_mode(qr_mode)
