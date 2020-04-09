# https://stackoverflow.com/a/54755738/9577873

import threading

import Queue
import cv2
from LED.LED import ON_ORANGE_PI


# bufferless VideoCapture
class VideoCapture(object):
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = Queue.Queue()

        if ON_ORANGE_PI:
            self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.w = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
            self.h = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print
                "[ERROR]: Cannot read frame, video capture stopped"
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except Queue.Empty:
                    pass
            self.q.put(frame)

    def isOpened(self):
        return self.cap.isOpened()

    def read(self):
        return self.q.get()
