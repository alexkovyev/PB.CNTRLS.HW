# coding=utf-8
import Tkinter as tk
import tkMessageBox
import json
import os
import time
import tkFileDialog
import ttk
from math import cos, sin
import serial.tools.list_ports

# You should probably change this to import dispenser_main/LED/LEDMode.py
from LEDMode import LEDMode


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port for port, desc, hwid in sorted(ports)]


class Labeled_entry(tk.Frame):
    def __init__(self, parent, label, entry_var, numeric=True):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label, anchor="w")
        self.entry = tk.Entry(self, textvariable=entry_var)

        if numeric:
            validate_cmd = (self.register(self.validate_input),
                            '%d', '%P')
            self.entry.configure(validate='key', validatecommand=validate_cmd)

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="bottom", fill="x")

    @staticmethod
    def validate_input(action, value_if_allowed):
        if action is "0":  # backspace
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


class RGBEmtries(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.r_var = tk.StringVar()
        self.g_var = tk.StringVar()
        self.b_var = tk.StringVar()

        self.r_input = Labeled_entry(self, "R", self.r_var)
        self.g_input = Labeled_entry(self, "G", self.g_var)
        self.b_input = Labeled_entry(self, "B", self.b_var)

        self.r_input.grid(column=0, row=0)
        self.g_input.grid(column=0, row=1)
        self.b_input.grid(column=0, row=2)

    def is_ok(self):
        try:
            self.get_rgb()
            return True
        except ValueError:
            return False

    def get_rgb(self):
        return [int(x.get()) for x in [self.r_input, self.g_input, self.b_input]]

    def get_hex(self):
        return '#%02x%02x%02x' % tuple(self.get_rgb())

    def set(self, values):
        [x.set(v) for x, v in zip([self.r_var, self.g_var, self.b_var], values)]


class TextControl(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.text_var = tk.StringVar()
        self.text_input = Labeled_entry(self, "Текст", self.text_var, False)

        self.duration_var = tk.StringVar()
        self.duration_input = Labeled_entry(self, "Длительность (миллисекунд)", self.duration_var)

        self.size_var = tk.StringVar()
        self.size_input = Labeled_entry(self, "Размер", self.size_var)

        self.color_entries = RGBEmtries(self)

        self.text_input.grid(column=0, row=0, sticky="NSEW")
        self.duration_input.grid(column=0, row=1, sticky="NSEW")
        self.size_input.grid(column=0, row=2, sticky="NSEW")
        self.color_entries.grid(column=0, row=3, sticky="NSEW")

    def is_ok(self):
        return self.text_var.get() and self.duration_var.get() and self.size_var.get()

    def get(self):
        return self.text_var.get(), int(self.duration_var.get()), int(self.size_var.get()), self.color_entries.get_rgb()


class MediaControl(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.select_frame = tk.Frame(self)

        self.type_var = tk.StringVar()
        self.image_btn = tk.Radiobutton(self.select_frame, text="Изображение", variable=self.type_var, value="I")
        self.video_btn = tk.Radiobutton(self.select_frame, text="Видео", variable=self.type_var, value="V")

        self.name_var = tk.StringVar()
        self.name_input = Labeled_entry(self, "Имя", self.name_var, False)

        self.duration_var = tk.StringVar()
        self.duration_input = Labeled_entry(self, "Длительность (миллисекунд)", self.duration_var)

        self.image_btn.grid(column=0, row=0, sticky="NSEW")
        self.video_btn.grid(column=1, row=0, sticky="NSEW")

        self.select_frame.grid(column=0, row=0, sticky="NSEW")
        self.name_input.grid(column=0, row=1, sticky="NSEW")
        self.duration_input.grid(column=0, row=2, sticky="NSEW")

    def is_ok(self):
        return self.duration_var.get()

    def get(self):
        return self.type_var.get(), self.name_var.get(), int(self.duration_var.get())


class PortSelector(tk.Frame):
    def __init__(self, root, device):
        tk.Frame.__init__(self, root)

        self.device = device

        self.ports = []

        self.port_var = tk.StringVar()
        self.port_choice = tk.OptionMenu(self, self.port_var, "", *self.ports)

        self.connect_text_var = tk.StringVar()
        self.connect_text_var.set("Подключится")
        self.connect_btn = tk.Button(self, textvariable=self.connect_text_var, command=self.connect)
        self.refresh_btn = tk.Button(self, text="Обновить", command=self.update_ports_list)

        self.port_choice.grid(column=0, row=0)
        self.connect_btn.grid(column=1, row=0)
        self.refresh_btn.grid(column=2, row=0)

    def set_options(self, options):
        if self.port_var.get() not in options:
            self.port_var.set("")

        self.port_choice['menu'].delete(0, 'end')  # clear

        for choice in options:
            self.port_choice['menu'].add_command(label=choice, command=tk._setit(self.port_var, choice))

    def update_ports_list(self):
        # tkMessageBox.showinfo("Пожалуйста, подождите...", "Идёт сканирование портов")
        top = tk.Toplevel(self, width=500)
        top.title('Пожалуйста, подождите...')
        top.geometry("350x30+30+30")
        # tk.Message(top, text="Идёт сканирование портов").pack(expand=True)
        tk.Label(top, text="Идёт сканирование портов").pack(anchor="center", fill="both")
        self.update_idletasks()

        ports = list_serial_ports()

        for port in ports:
            self.device.manager.bridge.port = port
            self.device.manager.bridge.open()
            time.sleep(2)

            self.device.ping()
            arrived = self.device.manager.wait_for_new_message(2)
            if not arrived:
                ports.remove(port)
            self.device.manager.bridge.close()

        self.set_options(ports)

        top.destroy()

    def connect(self):
        if not self.device.manager.bridge.isOpen():
            try:
                self.device.manager.bridge.port = self.port_var.get()
                self.device.manager.bridge.open()
                self.connect_text_var.set("Отключится")
                self.port_choice["state"] = "disabled"
            except serial.serialutil.SerialException as e:
                print "Cannot connect to port {}: {}".format(self.device.manager.bridge.port, e.strerror)
                self.update_ports_list()
        else:
            self.device.manager.bridge.close()
            self.port_choice["state"] = "normal"
            self.connect_text_var.set("Подключится")


class GUI:
    def __init__(self, device):
        self.device = device

        self.window = tk.Tk()
        self.window.configure(background='white')

        self.port_selector = PortSelector(self.window, self.device)
        self.port_selector.pack()

        self.tabs = ttk.Notebook(self.window)

        self.strip_mode_params = Mode_inputs(self.tabs)
        self.text_control = TextControl(self.tabs)
        self.media_control = MediaControl(self.tabs)
        # self.qr_mode_params = Mode_inputs(self.tabs)
        # self.mode_params.pack()
        self.tabs.add(self.strip_mode_params, text="лента")
        self.tabs.add(self.text_control, text="текст")
        self.tabs.add(self.media_control, text="медиа")
        # self.tabs.add(self.qr_mode_params, text="QR")

        self.tabs.pack(expand=1, fill="both")

        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Сохранить", command=self.save)
        self.file_menu.add_command(label="Загрузить", command=self.load)
        self.file_menu.add_command(label="Показать", command=self.send_data)
        self.menubar.add_cascade(label="Файл", menu=self.file_menu)

        self.window.mainloop()

    def send_data(self):

        try:
            current_tab = self.tabs.index("current")

            if current_tab == 0:
                self.device.demo_light_mode(self.strip_mode_params.get_led_mode())
            elif current_tab == 1:
                self.device.set_text(*self.text_control.get())
            elif current_tab == 2:
                media = self.media_control.get()
                if media[0] == "I":
                    self.device.set_dispaly_image(media[1], media[2])
                else:
                    self.device.set_display_video(media[1], media[2])
        except ValueError:
            pass

    def save(self):
        file_path = tkFileDialog.asksaveasfilename(initialdir=os.getcwd(), title="Save",
                                                   filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if file_path:
            led_mode = self.strip_mode_params.get_led_mode()
            data = {
                "led": led_mode.__dict__
            }

            if self.text_control.is_ok():
                text_data = self.text_control.get()
                text_keys = ["text", "duration", "size", "color"]
                data["text"] = dict(zip(text_keys, text_data))

            if self.media_control.is_ok():
                media_data = self.media_control.get()
                media_keys = ["type", "name", "duration"]
                data["media"] = dict(zip(media_keys, media_data))

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

    def load(self):
        file_path = tkFileDialog.askopenfilename(initialdir=os.getcwd(), title="Open",
                                                 filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if file_path:
            with open(file_path, "r") as f:
                j = json.load(f)
                led_mode = LEDMode()
                led_mode.__dict__ = j["led"]

                if "text" in j:
                    text_vars = [x for x in self.text_control.__dict__.keys() if x.endswith("_var")]
                    text_vars.append("color_entries")
                    for var in text_vars:
                        getattr(self.text_control, var).set(j["text"][var.split("_")[0]])

                if "media" in j:
                    media_vars = [x for x in self.media_control.__dict__.keys() if x.endswith("_var")]
                    for var in media_vars:
                        getattr(self.media_control, var).set(j["media"][var.split("_")[0]])

                self.strip_mode_params.set_led_mode(led_mode)