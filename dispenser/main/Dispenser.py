# coding=utf-8
import threading
from datetime import datetime

import cv2

import Validators
from LED.LED import LED, ON_ORANGE_PI, LEDMode
from VideoCapture import VideoCapture
from gui.GUI import MainGUI, current_ms_time
from interfacing.InterfacingManager import InterfacingManager
from interfacing.Message.Message import Message
from interfacing.Validator import Validator
from littering.LitteringDetector import LitteringDetector
from qr.QR_scanner import QRScanner


class Dispenser(threading.Thread):
    main_node_name = "PC"

    def __init__(self, serial_port="/dev/ttyS0"):
        super(Dispenser, self).__init__()

        self.node_name = "Dispenser"

        self.gui = MainGUI()
        self.led = LED()
        self.littering_detector = LitteringDetector()
        if ON_ORANGE_PI:
            self.qr_scanner = QRScanner("/dev/ttyS2")

        cap_id = 0
        if ON_ORANGE_PI:
            cap_id = 1
        self.video_capture = VideoCapture(cap_id)
        if not self.video_capture.isOpened():
            print "[ERROR]: Cannot open video capture on", cap_id

        self.interfacing = InterfacingManager(serial_port, self.node_name)

        self.images_directory = "photos"
        self.video_directory = "videos"

        self.last_action = current_ms_time()
        self.idle_time = 6000  # ms

        self.add_callbacks()
        self.add_validators()

        self.dispensed_id = None

        self.die = False

        self.led.die = self.die
        if ON_ORANGE_PI:
            self.qr_scanner.die = self.die
        self.interfacing.die = self.die

    def add_light_mode(self, message):
        mode = LEDMode()
        parameters = message.parameters.parameters
        mode.colors = [bool(int(x)) for x in parameters[1:4]]
        mode.min_val = int(parameters[4])
        mode.max_val = int(parameters[5])
        mode.min_time = float(parameters[6])
        mode.rise_time = float(parameters[7])
        mode.max_time = float(parameters[8])
        mode.decrease_time = float(parameters[9])
        mode.max_circles = int(parameters[10])
        self.led.add_mode(parameters[0], mode)

    def set_light_mode(self, message):
        self.led.set_mode(message.parameters.parameters[0])

    def set_display_text(self, message):
        # TODO: implement other parameters - size and color
        self.gui.set_text(message.parameters[0], int(message.parameters[1]))

    def set_display_image(self, message):
        self.gui.set_image(message.parameters.parameters[0], int(message.parameters[1]))

    def set_display_video(self, message):
        self.gui.set_video(message.parameters.parameters[0], int(message.parameters[1]))

    def is_littered(self, message):
        res = Message()
        res.header.node_name = Dispenser.main_node_name
        res.header.command_name = message.header.command_name
        if not self.video_capture.isOpened():
            res.parameters.append(1)
        else:
            img = self.video_capture.read()
            littered = self.littering_detector(img)
            res.parameters.append(int(littered))
        self.interfacing.send(res)

    def will_dispense(self, message):
        img = self.video_capture.read()
        self.littering_detector.train_background(img)

    def dispensed(self, message):
        # img = self.video_capture.read()
        # img_name = "{}/{}_{}.jpg".format(self.images_directory, message.parameters.parameters[0],
        #                                 datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        # cv2.imwrite(img_name, img)
        self.dispensed_id = message.parameters.parameters[0]

    def add_light_mode_validators(self):
        name_validator = Validator(Validators.check_str, 0)
        rgb_validator = Validator(Validators.check_bool, 1, 4)
        min_max_validator = Validator(Validators.check_color_val, 4, 6)
        seconds_validator = Validator(Validators.check_seconds, 6, 11)  # it will also validate max_circles
        self.interfacing.validators.add("add_light_mode",
                                        [name_validator, rgb_validator,
                                         min_max_validator, seconds_validator])

    def set_light_mode_validators(self):
        name_validator = Validator(Validators.check_str, 0)
        self.interfacing.validators.add("set_light_mode", name_validator)

    def set_display_text_validators(self):
        time_validator = Validator(Validators.check_seconds, 1)
        size_validator = Validator(Validators.is_positive_int, 2)
        rgb_validator = Validator(Validators.check_color_val, 3, 6)
        self.interfacing.validators.add("set_display_text", [time_validator, size_validator, rgb_validator])

    def set_display_image_validators(self):
        name_validator = Validator(Validators.check_str, 0)
        time_validator = Validator(Validators.check_seconds, 1)
        self.interfacing.validators.add("set_display_image", [name_validator, time_validator])

    def set_display_video_validators(self):
        name_validator = Validator(Validators.check_str, 0)
        end_time_validator = Validator(Validators.check_seconds, 1)
        self.interfacing.validators.add("set_display_video",
                                        [name_validator, end_time_validator])

    def dispensed_validators(self):
        id_validator = Validator(Validators.check_str, 0)
        self.interfacing.validators.add("dispensed", id_validator)

    def add_validators(self):
        self.add_light_mode_validators()
        self.set_light_mode_validators()

        self.set_display_text_validators()
        self.set_display_image_validators()
        self.set_display_video_validators()

        self.dispensed_validators()

    def _update_last_action(self, message):
        self.last_action = current_ms_time()

    def add_callbacks(self):
        self.interfacing.callacks.add("add_light_mode", self.add_light_mode)
        self.interfacing.callacks.add("set_light_mode", self.set_light_mode)

        self.interfacing.callacks.add("set_display_text", self.set_display_text)
        self.interfacing.callacks.add("set_display_image", self.set_display_image)
        self.interfacing.callacks.add("set_display_video", self.set_display_video)

        self.interfacing.callacks.add("is_littered", self.is_littered)
        self.interfacing.callacks.add("will_dispense", self.will_dispense)
        self.interfacing.callacks.add("dispensed", self.dispensed)

        self.interfacing.callacks.add("*", self._update_last_action)

    @staticmethod
    def validate_qr_code(code):
        if code != "123":
            return False
        return True

    def qr_handler_routine(self):
        while not self.die:
            if not self.qr_scanner.empty():
                self._update_last_action(None)
                qr_data = self.qr_scanner.get()
                if self.validate_qr_code(qr_data):
                    message = Message()
                    message.header.node_name = Dispenser.main_node_name
                    message.header.command_name = "qr_scanned"
                    message.parameters.append(qr_data)
                    self.interfacing.send(message)
                else:
                    print "Wrong QR code format:", qr_data
                    if "wrong_qr" in self.led.modes:
                        self.gui.set_text("Ошибка при считывании QR кода.\nПожалуйста, попробуйте снова.", 3000)
                        self.led.set_mode("wrong_qr")

    def idle_handler_routine(self):
        while not self.die:
            if current_ms_time() - self.last_action > self.idle_time:
                if "idle" in self.led.modes and self.led.current_mode.value not in ["wait", "dispensed"]:
                    self.led.set_mode("idle")

    def video_capture_routine(self):
        while not self.die:
            if self.dispensed_id:
                print "Waiting for pick up:", self.dispensed_id
                vid_name = "{}/{}_{}.avi".format(self.video_directory, self.dispensed_id,
                                                 datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
                if not ON_ORANGE_PI:
                    furcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
                else:
                    furcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                video_writer = cv2.VideoWriter(vid_name, furcc, 5,
                                               (self.video_capture.w, self.video_capture.h))
                littered = True
                i = 0
                while littered:
                    img = self.video_capture.read()
                    if not i % 3:
                        littered = self.littering_detector(img)
                    video_writer.write(img)
                    i += 1
                    cv2.waitKey(2)
                for i in range(5):
                    img = self.video_capture.read()
                    video_writer.write(img)
                    cv2.waitKey(1)
                video_writer.release()
                print "Video saved:", vid_name
                self.dispensed_id = None

                # I don`t want to add another thread for that
                msg = Message()
                msg.header.node_name = Dispenser.main_node_name
                msg.header.command_name = "picked_up"
                self.interfacing.send(msg)

    def run(self):
        self.led.start()
        self.interfacing.start()
        if ON_ORANGE_PI:
            self.qr_scanner.start()

            qr_handler_thread = threading.Thread(target=self.qr_handler_routine)
            qr_handler_thread.daemon = True
            qr_handler_thread.start()

        idle_handler_thread = threading.Thread(target=self.idle_handler_routine)
        idle_handler_thread.daemon = True
        idle_handler_thread.start()

        video_capture_thread = threading.Thread(target=self.video_capture_routine)
        video_capture_thread.daemon = True
        video_capture_thread.start()

    def join(self):
        self.die = True
        threading.Thread.join(self, 3)
