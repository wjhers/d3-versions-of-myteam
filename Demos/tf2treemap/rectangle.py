
import numpy as np

EPSILON = 1e-6

class Rect(object):
    def __init__(self):
        self.r_id = None
        self.size = None
        self.x1 = None
        self.area = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    def setAttr(self, id, size, area, x1, y1, x2, y2):
        self.r_id = int(id)
        # size of rect (size != width * height)
        self.size = size
        self.area = area
        # left upper
        self.x1 = x1
        self.y1 = y1
        # right lower (x2 > x1 & y2 > y1)
        self.x2 = x2
        self.y2 = y2


    @property
    def width(self):
        return self.x2-self.x1
    @property
    def height(self):
        return self.y2-self.y1
    @property
    def aspect_ratio(self):
        return max(float(self.width/self.height),float(self.height/self.width))

    def tomove(self,delta_x1, delta_y1, delta_x2, moving):
        # allow movement
        if moving:
            self.x1 += delta_x1
            self.y1 += delta_y1
            self.x2 += delta_x2
            # (x2 > x1 & y2 > y1)
            width = self.x2 - self.x1
            self.y2 = self.y1 + float(self.area / width)
    
    @property
    def listLocations(self):
        return np.asarray([self.x1, self.y1, self.x2, self.y2])
    
    @property
    def listObservations(self):
        return np.asarray([self.x1, self.y1, self.x2, self.y2, self.aspect_ratio])