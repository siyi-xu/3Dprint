from SplitRegion import *


# 主要是通过上述文件完成平行填充路径生成。先通 过 rotatePolygons 函数实现轮廓按输入角度旋转，
# 然后通过 SplitRegion 函数对轮廓进行填充 区域分割，得到若干个单连通区域的轮廓。
# 通过 genScanYs 函数得到对应轮廓范围的 y 轴扫 描线组，
# 用 genHatches 函数截交后用 linkLocalHatches 函数连接成 Z 字形路径，并用 rotatePolygons 反旋转回原角度
class GenDpPath:
    def __init__(self, polygons, interval, angle):
        self.polygons = rotatePolygons(polygons, angle)
        self.splitPolys = splitRegion(self.polygons)
        self.interval = interval
        self.angle = angle
        self.ys = self.genScanYs(self.splitPolys)
        self.segses = genHatches(self.splitPolys, self.ys)
        self.polys = []

    def genScanYs(self, Polys):
        yMin, yMax = float('inf'), float('-inf')  # 获取旋转后多边形最低和最高值
        for i in range(len(Polys)):
            for pt in Polys[i].points:
                yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
        ys = []  # 存储扫描线高度
        y = yMin + self.interval  # 其实高度
        while y < yMax:  # 根据输入间距生成高度列表ys
            ys.append(y)
            y += self.interval
        return ys

    def generate(self):
        for poly in self.splitPolys:
            segs = genHatches([poly], self.ys)
            if len(segs) > 0:
                path = linkLocalHatches(segs)
                self.polys.append(path)
        self.polys = rotatePolygons(self.polys, -self.angle)
        return self.polys

    def generateEx(self, ys=None, center=None):  # 定义generateEx函数
        rotPolys = rotatePolygons(self.polygons, -self.angle, center)  # 旋转多边形
        if ys is None:  # 如果参数ys为None
            ys = self.genScanYs(rotPolys)  # 则根据多边形生成独立的ys
        self.splitPolys = splitRegion(rotPolys)  # 分区生成单连同区域
        paths = []  # 定义路径序列
        for poly in self.splitPolys:  # 对每个单连通区域生成路径
            segs = genHatches([poly], ys)  # 生成平行填充线段
            if len(segs) > 0:
                path = linkLocalHatches(segs)  # 连接单连通区域内填充线段
                paths.append(path)
        return rotatePolygons(paths, self.angle, center)  # 反向旋转并返回路径


def genDpPath(polygons, interval, angle):
    r = GenDpPath(polygons, interval, angle)
    # print(r.polygons)
    return r.generate()


def genDpPathEx(polygons, interval, angle, ys=None, center=None):  # generateEx接口函数
    return GenDpPath(polygons, interval, angle).generateEx(ys, center)
