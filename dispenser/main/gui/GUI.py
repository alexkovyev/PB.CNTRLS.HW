import Tkinter as tk
import ctypes
import os
import threading
import time
from PIL import ImageTk, Image

import vlc


def current_ms_time():
    return int(round(time.time() * 1000))


class MainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background='black')

        self.window.attributes('-fullscreen', True)
        self.window_width = self.window.winfo_screenwidth()
        self.window_height = self.window.winfo_screenheight()

        # self.window.overrideredirect(1)  # always on top

        self.label_text = tk.StringVar()
        self.label_widget = tk.Label(self.window, textvariable=self.label_text, bg="black", fg="white",
                                     font="Arial 34 bold")

        self.canvas = tk.Canvas(self.window, width=self.window_width, height=self.window_height)
        self.canvas.configure(background="black", highlightthickness=0)

        self.video_frame = tk.Frame(self.window, bg="black")
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
        self.vlc_instance, self.vlc_media_player_instance = self._create_vlc_instance()

        self.window.bind("<F11>", self.toggle_fullscreen)
        self.fullScreenState = True

        self.time_limits = {}

        time_routine_th = threading.Thread(target=self._time_routine)
        time_routine_th.daemon = True
        time_routine_th.start()

    def _create_vlc_instance(self):
        """Create a vlc instance; `https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html`"""
        vlc_instance = vlc.Instance()
        vlc_media_player_instance = vlc_instance.media_player_new()
        self.video_frame.update()
        return vlc_instance, vlc_media_player_instance

    def set_text(self, text, time_limit=0):
        self.hide_image()
        self.hide_video()
        self.show_label()
        self.time_limits["text"] = (current_ms_time(), time_limit)
        self.label_text.set(text)

    def show_label(self):
        self.label_widget.place(relx=.5, rely=.6, anchor="c")

    def hide_label(self):
        self.label_widget.place_forget()

    def _resize_img(self, img, uniform=True):
        if uniform:
            img_w, img_h = img.size
            ratio = min(float(self.window_width) / img_w, float(self.window_height) / img_h)
            img_w = int(img_w * ratio)
            img_h = int(img_h * ratio)

            return img.resize((img_w, img_h), Image.ANTIALIAS)
        else:
            return img.resize((self.window_width, self.window_height), Image.ANTIALIAS)

    def set_image(self, image_path, time_limit=0):
        self.hide_label()
        self.hide_video()
        self.show_image()
        self.time_limits["image"] = (current_ms_time(), time_limit)

        pil_img = Image.open(image_path)
        pil_img = self._resize_img(pil_img, True)

        self.window.image = ImageTk.PhotoImage(pil_img)  # https://stackoverflow.com/a/48757712/9577873
        self.canvas.create_image(self.window_width / 2, self.window_height / 2, image=self.window.image)

    def show_image(self):
        self.canvas.pack()

    def hide_image(self):
        self.canvas.pack_forget()

    def show_video(self):
        self.video_frame.pack(fill=tk.BOTH, expand=1)

    def hide_video(self):
        self.video_frame.pack_forget()
        self.vlc_media_player_instance.pause()

    def set_video(self, video_file, time_limit=0):
        self.hide_label()
        self.hide_image()
        self.show_video()
        self.time_limits["video"] = (current_ms_time(), time_limit)

        fullname = os.path.abspath(video_file)
        self.Media = self.vlc_instance.media_new(fullname)
        self.vlc_media_player_instance.set_media(self.Media)
        self.vlc_media_player_instance.set_xwindow(self.video_frame.winfo_id())
        self.vlc_media_player_instance.play()

    def _time_routine(self):
        while True:
            fn = None
            key = None
            if "video" in self.time_limits:
                key = "video"
                fn = self.hide_video
            elif "image" in self.time_limits:
                key = "image"
                fn = self.hide_image
            elif "text" in self.time_limits:
                key = "text"
                fn = self.hide_label

            if key is not None:
                limit = self.time_limits[key]
                if limit[1] != 0 and current_ms_time() - limit[0] >= limit[1]:
                    del self.time_limits[key]
                    fn()

    def toggle_fullscreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
