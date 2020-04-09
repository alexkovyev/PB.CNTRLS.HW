import cv2


# You should not update objects of this class with "=" operator
# Use "update" method instead to make "not_updated" counter work properly
# The fact that i can`t redefine assignment operator in python sucks
class Box(object):
    def __init__(self, box_tuple):
        self.x, self.y, self.w, self.h = (0, 0, 0, 0)
        self.update(box_tuple)

        self.not_updated = 0

    def __setattr__(self, key, value):
        if key in ["x", "y", "w", "h"]:
            self.not_updated = 0
        super(Box, self).__setattr__(key, value)

    def __repr__(self):
        return "[{}:{}, {}:{}, not updated for {} frames]".format(self.x, self.y, self.w, self.h, self.not_updated)

    # top-left
    def tl(self):
        return self.x, self.y

    # top-right
    def tr(self):
        return self.x + self.w, self.y

    # bottom-left
    def bl(self):
        return self.x, self.y + self.h

    # bottom-right
    def br(self):
        return self.x + self.w, self.y + self.h

    def edges(self):
        return [self.tl(), self.tr(), self.bl(), self.br()]

    def center(self):
        return self.x + self.w / 2, self.y + self.h / 2

    # returns rectangle in opencv format
    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def update(self, new_val):
        if isinstance(new_val, tuple):
            self.x, self.y, self.w, self.h = new_val
        elif isinstance(new_val, Box):
            new_val.not_updated = 0
            self.__dict__.update(new_val.__dict__)

    def find_nearest(self, boxes, max_dist=25):
        min_dist = 0
        box_center = self.center()
        res = None
        for i, b in enumerate(boxes):
            b_center = b.center()
            dist = get_distance(box_center, b_center)
            if max_dist > dist >= min_dist:
                max_dist = dist
                res = i
        return res

    # i think, that it is also not the best implementation ever,
    # but i don`t want to spend time doing something more elegant
    def intersects(self, other):
        edges_a = self.edges()
        edges_b = other.edges()
        rect_a = self.get_rect()
        rect_b = other.get_rect()
        for edge_a in edges_a:
            if rect_contains(rect_b, edge_a):
                return True
        for edge_b in edges_b:
            if rect_contains(rect_a, edge_b):
                return True
        return False

    def draw(self, img, color=(0, 255, 0)):
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), color, 2)
