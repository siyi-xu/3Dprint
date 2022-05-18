from GeomBase import *


class Line:
    def __init__(self, P, V):
        self.P = P.clone()  # 直线经过的点,类型为Point3D
        # self.P = P # 这样写后面会被再次赋值时改变初始点
        self.V = V.clone().normalized()  # 直线方向向量,类型为Vector3D,单位向量

    def __str__(self):
        return "Line\nP %s\nV %s\n" % (str(self.P), str(self.V))
