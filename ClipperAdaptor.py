import math
from pyclipper import *
from Polyline import *


# 对 clipper 库的调用

class ClipperAdaptor:  # 定义Clipper适配器类
    def __init__(self, digits=7):  # 初始化函数
        self.f = math.pow(10, digits)  # 数值精度，默认为7位小数
        self.arcTolerance = 0.005  # 圆弧精度，默认为0.005mm

    def toPath(self, poly):  # 将Polyline转化为Path
        path = []
        for pt in poly.points:
            path.append((pt.x * self.f, pt.y * self.f))  # 放大点坐标
        return path

    def toPaths(self, polys):  # 函数toPath的复数形式
        paths = []
        for poly in polys: paths.append(self.toPath(poly))
        return paths

    def toPoly(self, path, z=0, closed=True):  # 将Path转化为Polyline
        poly = Polyline()
        for tp in path:
            poly.addPoint(Point3D(tp[0] / self.f, tp[1] / self.f, z))  # 缩小点坐标
        if len(path) > 0 and closed:  # 如果封闭，则将起点添加到轮廓
            poly.addPoint(poly.startPoint())  # 最后一点
        return poly

    def toPolys(self, paths, z=0, closed=True):  # 函数toPoly的复数形式
        polys = []
        for path in paths:
            polys.append(self.toPoly(path, z, closed))
        return polys

    def offset(self, polys, delta, jt=JT_SQUARE):  # 偏函数，输入Polyline列表
        pco = PyclipperOffset()
        pco.ArcTolerance = self.arcTolerance * self.f  # 指定pco的圆弧精度，放大
        # print("len(polys)_in",len(polys))
        pco.AddPaths(self.toPaths(polys), jt, ET_CLOSEDPOLYGON)
        sln = pco.Execute(delta * self.f)  # 偏置距离也须同时放大

        return self.toPolys(sln, polys[0].points[0].z)  # 返回Polyline列表
