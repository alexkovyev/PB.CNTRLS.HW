import itertools
import numpy as np

import cv2

from Box import Box
from dispenser.main.LED.LED import ON_ORANGE_PI
from utils import *


# maybe, it is not the best way to do that, but it is ok for now
def get_minimum_distance(a, b):
    edges_a = a.edges()
    edges_b = b.edges()
    distances = []
    for edge_a in edges_a:
        for edge_b in edges_b:
            distances.append(get_distance(edge_a, edge_b))

    multiplier = -1 if a.intersects(b) else 1
    return min(distances) * multiplier


def merge_boxes(boxes, max_dist=100):
    while True:
        found = False
        for ra, rb in itertools.combinations(boxes, 2):
            if get_minimum_distance(ra, rb) < max_dist:
                if ra in boxes:
                    boxes.remove(ra)
                if rb in boxes:
                    boxes.remove(rb)
                new_rect = union(ra.get_rect(), rb.get_rect())
                new_box = Box(new_rect)
                new_box.not_updated = max(ra.not_updated, rb.not_updated)
                boxes.append(new_box)
                found = True
                break
        if not found:
            break

    return boxes


class LitteringDetector(object):
    def __init__(self):
        if ON_ORANGE_PI:
            self.background_sub = cv2.createBackgroundSubtractorMOG2()
        else:
            self.background_sub = cv2.BackgroundSubtractorMOG2()

        self.realtime = False

        self.min_contour_area = 150
        self.min_bbox_size = (100, 100)
        self.min_littered_frames = 5 if self.realtime else 0

        self.littered_frames = 0

        self.bg = None

        self.boxes = []

    def get_foreground(self, img):
        fg_mask = self.background_sub.apply(img, None, 0)
        _, res = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
        return res

    def train_background(self, background):
        img = self.normalize_image(background)
        self.background_sub.apply(img, None, 1)

    # https://stackoverflow.com/questions/44752240/how-to-remove-shadow-from-scanned-images-using-opencv/44752405#44752405
    @staticmethod
    def normalize_image(img):
        rgb_planes = cv2.split(img)

        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)

        result_norm = cv2.merge(result_norm_planes)

        # https://stackoverflow.com/a/41075028/9577873
        '''
        lab = cv2.cvtColor(result_norm, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        '''
        return result_norm

    @staticmethod
    def prepare_mask(mask):
        opening_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closing_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        res = cv2.erode(mask, erode_kernel)
        res = cv2.morphologyEx(res, cv2.MORPH_OPEN, opening_kernel)
        res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, closing_kernel)
        # res = cv2.dilate(res, opening_kernel)

        return res

    def extract_contours(self, mask):
        if not ON_ORANGE_PI:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_contour_area]
        return contours

    @staticmethod
    def get_bounding_boxes(contours):
        res = []
        for contour in contours:
            bound = cv2.boundingRect(contour)
            res.append(Box(bound))
        return res

    def update_boxes(self, boxes):
        if len(self.boxes) == 0 or not self.realtime:
            self.boxes = boxes
        elif self.realtime:
            boxes_updated = {b: False for b in self.boxes}
            for box in boxes:
                nearest = box.find_nearest(self.boxes)
                if nearest is None:
                    self.boxes.append(box)
                else:
                    nearest_box = self.boxes[nearest]
                    boxes_updated[nearest_box] = True
                    nearest_box.update(box)

            for box, updated in boxes_updated.items():
                if not updated:
                    box.not_updated += 1

            for box in self.boxes:
                if box.not_updated >= 5:
                    self.boxes.remove(box)

        self.boxes = merge_boxes(self.boxes)

        for box in self.boxes[:]:
            if box.w < self.min_bbox_size[0] or box.h < self.min_bbox_size[1]:
                self.boxes.remove(box)

    @staticmethod
    def draw_boxes(img, boxes):
        for box in boxes:
            box.draw(img)

    def is_littered(self):
        if self.min_littered_frames > 0 and self.realtime:
            return self.littered_frames >= self.min_littered_frames
        else:
            return len(self.boxes) > 0

    def __call__(self, img):
        last_len = len(self.boxes)

        prepared_img = self.normalize_image(img)
        # cv2.imshow("prepared", prepared_img)
        fg_mask = self.get_foreground(prepared_img)
        # cv2.imshow("fg", fg_mask)
        mask = self.prepare_mask(fg_mask)
        # cv2.imshow("mask", mask)
        # cv2.waitKey(0)
        contours = self.extract_contours(mask)
        boxes = self.get_bounding_boxes(contours)
        self.update_boxes(boxes)

        # self.draw_boxes(img, self.boxes)
        # cv2.imshow("img", img)
        # cv2.waitKey(1)

        if len(self.boxes) > 0:
            self.littered_frames += 1
        else:
            if last_len > 0:
                self.littered_frames = self.min_littered_frames * 2
            if self.littered_frames > 0:
                self.littered_frames -= 1

        return self.is_littered()
