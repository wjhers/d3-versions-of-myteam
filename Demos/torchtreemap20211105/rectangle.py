
import numpy as np

class Rect(object):
    def __init__(self, size, area, height, width, x, y):
        '''
        矩形的定义：
        _size 是结点树节点的大小
        _area 是结点树节点对应矩形的面积
        _height_half 是矩形的高度的一半
        _width_half 是矩形的宽度的一半
        _x, _y 是矩形的中心坐标
        '''
        self._size = size
        self._area = area
        self._height_half = round(height/2)
        self._width_half = round(width/2)
        self._x = round(x)
        self._y = round(y)

    def getHeight(self):
        return 2 * self._height_half

    def getWidth(self):
        return 2 * self._width_half

    def getCenter(self):
        return np.array([self._x, self._y])

    def getSize(self):
        return self._size

    def getArea(self):
        return self._area

    def getChangeArea(self):
        return self.getHeight() * self.getWidth()

    def getAspectRatio(self):
        return max(self.getHeight()/self.getWidth(), self.getWidth()/self.getHeight())

    def getState(self):
        return np.array([self._x, self._y, self._height_half, self._width_half])

    def toMove(self, action_n_i):
        if action_n_i == 0:
            self._y -= 1
        elif action_n_i == 1:
            self._y += 1
        elif action_n_i == 2:
            self._x -= 1
        elif action_n_i == 3:
            self._x += 1
        elif action_n_i == 4:
            self._width_half += 1
        elif action_n_i == 5:
            self._width_half -= 1
        elif action_n_i == 6:
            self._height_half += 1
        elif action_n_i == 7:
            self._height_half -= 1

    def printInfo(self):
        print(f"size: {self.getSize()}")
        print(f"area: {self.getArea()}")
        print(f"changearea: {self.getChangeArea()}")
        print(f"height: {self.getHeight()}")
        print(f"width: {self.getWidth()}")
        print(f"center: {self.getCenter()}")
        print(f"aspect-ratio: {self.getAspectRatio()}")
        print(f"state: {self.getState()}")


def getSubRectInfoFromRoot(r_size, r_area, s_size):
    '''
    函数：getSubRectInfoFromRoot
    根据root矩形的size与sub矩形的size，获得sub矩形的信息
    '''
    if s_size <= r_size:
        s_area = round(r_area * (s_size / r_size))
        s_height = round(s_area**(1/2))
        s_width = s_height
        s_x = round(1/2 * (s_width))
        s_y = s_x
        return np.array([s_size, s_area, s_height, s_width, s_x, s_y], dtype=np.float32)
    else:
        return "error"