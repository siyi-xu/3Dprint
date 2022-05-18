from GeomBase import *


# 也是STL.py的基础
class Polyline:
    def __init__(self):
        self.points = []

    def __str__(self):
        if self.count() > 0:
            return 'Polyline\nPoint number:%s\nStart %s\nEnd %s\n' \
                   % (self.count(), str(self.startPoint()), str(self.endPoint()))
        else:
            return "Polyline\nPoint number: 0\n"

    def clone(self):
        poly = Polyline()
        for pt in self.points:
            poly.addPoint(pt.clone)
        return poly

    def count(self):
        return len(self.points)

    def addPoint(self, pt):
        self.points.append(pt)

    def addTuple(self, tuple):
        self.points.append(Point3D(tuple[0], tuple[1], tuple[2]))

    def raddPoint(self, pt):
        self.points.insert(0, pt)

    def removePoint(self, index):
        return self.points.pop(index)

    def __add__(self, other):
        p = self.clone()
        for i in range(other.count()):
            p.addPoint(other.points[i])
        return p

    def add_tail(self, list):
        for i in range(len(list)):
            self.addPoint(list[i])

    def add_head(self, list):
        for i in range(len(list) - 1, -1, -1):
            self.points.insert(0, list[i])

    def insert(self, pt, other):
        other.points.append(self.points[pt])
        for i in range(other.count() - 1, -1, -1):
            self.points.insert(pt + 1, other.points[i])

    def startPoint(self):
        return self.points[0]

    def endPoint(self):
        return self.points[-1]

    def isclose(self):
        if self.count() > 1 and self.startPoint() == self.endPoint():
            return True
        else:
            return False

    def getArea(self):
        point_num = self.count()
        if (point_num < 3): return 0.0
        s = self.points[0].y * (self.points[point_num - 1].x - self.points[1].x)
        for i in range(1, point_num):
            s += self.points[i].y * (self.points[i - 1].x - self.points[(i + 1) % point_num].x)
        return abs(s / 2.0)

    def makeCCW(self):
        d = 0
        for i in range(self.count() - 1):
            d -= (self.points[i + 1].y + self.points[i].y) * (self.points[i + 1].x - self.points[i].x)
        if d < 0:
            self.points.reverse()

    def makeCW(self):
        d = 0
        for i in range(self.count() - 1):
            d -= (self.points[i + 1].y + self.points[i].y) * (self.points[i + 1].x - self.points[i].x)
        if d > 0:
            self.points.reverse()

    def multiply(self, m):  # 对对象本身变换，作用一个矩阵m
        for pt in self.points:
            pt.multiply(m)

    def multiplied(self, m):  # 作用矩阵m，产生一个新的多段线对象
        poly = Polyline()
        for pt in self.points:
            poly.addPoint(pt * m)
        return poly


if __name__ == "__main__":
    pl1 = Polyline()
    pl2 = Polyline()
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(1, 1, 1)
    p3 = Point3D(2, 2, 2)
    p4 = Point3D(0, 0, 0)
    pl1.addPoint(p1)
    pl1.addPoint(p2)
    pl2.addPoint(p3)
    pl2.addPoint(p4)
    pl1.insert(0, pl2)

    print(pl1.points[1])
