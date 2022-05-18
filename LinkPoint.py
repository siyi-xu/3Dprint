from GeomBase import Point3D  # 导入Point3D类
from Polyline import *


# 为拼接的基础


class LinkPoint():  # 链接点类，LinkPoint
    def __init__(self, pnt3d, digits=7):  # 根据Point3D对象初始化
        self.x = round(pnt3d.x, digits)  # 点的x、y、z坐标
        self.y = round(pnt3d.y, digits)
        self.z = round(pnt3d.z, digits)
        self.other = None  # 指针，指向线段另一个端点
        self.used = False  # 点是否已经被使用
        self.index = 0  # 点在列表中的序号

    def __str__(self):  # 转字符串函数，方便调试
        return 'LinkPoint:used:%s\nself(%s,%s,%s)\nother(%s,%s,%s)\nlinkedto:%s' % (
        self.used, self.x, self.y, self.z, self.other.x, self.other.y, self.other.z, self.other.index)

    def toPoint3D(self):  # LinkPoint转化为Point3D对象
        return Point3D(self.x, self.y, self.z)

    def __eq__(self, other):
        if other == None:
            return False
        if self.toPoint3D() == other.toPoint3D() and self.other.toPoint3D() == other.other.toPoint3D():
            return True
        else:
            return False


if __name__ == "__main__":
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(1, 1, 1)
    p3 = Point3D(0, 0, 0)
    p4 = Point3D(3, 3, 3)

    lp1, lp2 = LinkPoint(p1), LinkPoint(p2)
    lp1.other, lp2.other = lp2, lp1
    lp3, lp4 = LinkPoint(p3), LinkPoint(p4)
    lp3.other, lp4.other = lp4, lp3
    print(lp3 == lp2)
