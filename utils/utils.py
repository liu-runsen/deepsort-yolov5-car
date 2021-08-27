#_*_coding:UTF-8_*_
'''
@Author：Runsen
判断点是不是在矩形中
'''
import numpy as np
import cv2


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)


class Line:
    def __init__(self, p1, p2):

        self.p1 = p1
        self.p2 = p2

        self.k = (p2.y - p1.y) / (p2.x - p1.x) if p1.x != p2.x else None
        self.b = -p1.x * (p2.y - p1.y) / (p2.x - p1.x) + p1.y if p1.x != p2.x else None

    def intersection(self, line2):

        # 两直线平行
        if self.is_vertical() and line2.is_vertical():
            return None

        if self.k == line2.k:
            return None

        # 相交

        # 有其中一条垂直
        if self.is_vertical():
            x = self.p1.x
            y = round(line2.k * x + line2.b, 2)
        elif line2.is_vertical():
            x = line2.p1.x
            y = round(self.k * x + self.b, 2)
        else:
            # 一般情况
            x = round((self.b - line2.b) / (line2.k - self.k), 2)
            y = round(self.k * x + self.b, 2)

        # 点在线段上：x在线段的范围内
        r1 = (self.p2.x, self.p1.x) if self.p1.x >= self.p2.x else (self.p1.x, self.p2.x)
        r2 = (line2.p2.x, line2.p1.x) if line2.p1.x >= line2.p2.x else (line2.p1.x, line2.p2.x)
        if not (r1[0] <= x <= r1[1] and r2[0] <= x <= r2[1]):
            return None

        return Point(x, y)

    def is_horizontal(self):

        return self.p1.y == self.p2.y

    def is_vertical(self):

        return self.p1.x == self.p2.x

    def __repr__(self):
        return "[{}->{}, k={}, b={}]".format(self.p1, self.p2, self.k, self.b)


class Polygen:

    def __init__(self, *points):
        self.points = points
        self.lines = []
        for i in range(-1, len(points) - 1):
            self.lines.append(Line(points[i], points[i + 1]))

    def contains(self, point):
        point_b = Point(point.x + 100000000, point.y)  # 这个值尽量大，因为暂时不支持射线

        line2 = Line(point, point_b)
        line3 = Line(Point(2, -1), Point(2, 3))

        return len(
            list(filter(lambda p: p is not None, list(map(lambda l: l.intersection(line2), self.lines))))) % 2 == 1


def line_resize(line):
    '''
    返回 960 * 540 的 resize line的值为 1
    :param line:
    :return:
    '''
    mask_image = np.zeros((1080, 1920), dtype=np.uint8)
    line_value = cv2.fillPoly(mask_image, [np.array(line, np.int32)], color=1)[:, :, np.newaxis]
    line_value_resize = cv2.resize(line_value, (960, 540))
    return line_value_resize


def poly(poly_list):
    '''
    poly_list :x1, y1, x2, y2, x3, y3, x4, y4
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param x3:
    :param y3:
    :param x4:
    :param y4:
    :return:
    '''
    x1 = poly_list[0]
    y1 = poly_list[1]
    x2 = poly_list[2]
    y2 = poly_list[3]
    x3 = poly_list[4]
    y3 = poly_list[5]
    x4 = poly_list[6]
    y4 = poly_list[7]
    return Polygen(Point(x1, y1),
                   Point(x2, y2),
                   Point(x3, y3),
                   Point(x4, y4))




