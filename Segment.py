from GeomBase import *


# 也是STL.py的基础
class Segment:
    def __init__(self, A, B):  # 线段两端点A,B
        self.A = A.clone()
        self.B = B.clone()

    def __str__(self):  # 线段被print时的行为
        return "Line\nP %s\nV %s\n" % (str(self.A), str(self.B))

    def length(self):  # 计算线段长度
        return self.A.distance(self.B)

    def direction(self):  # 计算线段方向
        return self.A.pointTo(self.B)

    def swap(self):  # 交换线段两端点
        self.A, self.B = self.B, self.A

    def multiply(self, m):  # 对对象本身变换，作用一个矩阵m
        self.A = self.A.multiplied(m)
        self.B = self.B.multiplied(m)

    def multiplied(self, m):  # 作用矩阵m，产生一个新的线段对象
        seg = Segment(self.A, self.B)
        seg.multiply(m)
        return seg
