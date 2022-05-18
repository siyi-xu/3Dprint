from ClipperAdaptor import *
from PolyPcrSeeker import *


# 实现对层内轮廓偏置曲线的生成，实现方面主要是通过控制偏置距离 小于填充带宽的情况下，
# 不断调用 ClipperAdaptor 文件中的同名函数 offset，获取一系列偏 置曲线。
# 然后通过 linkToParent 函数，得到子轮廓起始点距离父轮廓的最近点，将两点距离作为 轮廓间最近距离，同时也意味着两点连线是轮廓的最近连接线
class GenCpPath:  # 定义GenCpPath类
    def __init__(self, boundaries, interval, shellThk):  # 输入：轮廓、偏置距离、填充带宽
        self.boundaries = boundaries  # 打印区域边界轮廓
        self.interval = interval  # 工艺参数：偏置距离（喷头直径）
        self.shellThk = shellThk  # 工艺参数：填充带宽（外壳厚度）
        self.arcTolerance = 0.005  # 工艺参数：圆弧精度
        self.jointType = JT_SQUARE  # 工艺参数：衔接类型
        self.offsetPolyses = []  # 临时存储的中间偏置曲线列表
        self.inpolys = []
        self.paths = []  # 最终输出的轮廓平行路径列表
        self.offset()  # 调用连续偏置路径生成函数
        self.linkLocalOffsets()  # 调用路径连接函数

    def offset(self):  # 定义连续偏置路径生成函数
        ca = ClipperAdaptor()  # 定义Clipper适配器对象
        ca.arcTolerance = self.arcTolerance  # 设置圆弧精度（使用圆弧衔接）
        delta = self.interval / 2  # 首次偏置距离
        polys = ca.offset(self.boundaries, -delta, self.jointType)
        self.offsetPolyses.append(polys)  # 偏置曲线存放在offsetPolys中
        self.inpolys = polys
        while math.fabs(delta) < self.shellThk:  # 循环直至偏置距离大于填充带宽
            delta += self.interval
            polys = ca.offset(self.boundaries, -delta, self.jointType)
            if polys is None or len(polys) == 0: break  # 已到偏置区域中心，则退出
            self.offsetPolyses.append(polys)
            self.inpolys = polys

    def linkLocalOffsets(self):  # 定义路径连接函数
        polys = seekPolyPcr(self.offsetPolyses)
        while polys[-1].depth != 0:
            self.linkToParent(polys[-1], polys[-1].parent)
            del polys[-1]
        self.paths = polys

    def linkToParent(self, child, parent):  # 将输入的子曲线（child）桥接到父曲线（parent）上
        pt = 0
        min_dis = child.startPoint().distance(parent.startPoint())
        for i in range(parent.count()):
            dis = child.startPoint().distance(parent.points[i])
            if dis < min_dis:
                pt = i
                min_dis = dis
        parent.insert(pt, child)

    def genScanYs(self):
        pass


def genCpPath(boundaries, interval, shellThk):
    return GenCpPath(boundaries, interval, shellThk)


'''
if __name__ == '__main__':  # 测试main函数入口,测的是正方形
    subject = [(0, 0), (100, 0), (100, 70), (0, 70)]  # 创建subject轮廓subject，正方形
    clip = [(30, 50), (70, 50), (70, 100), (30, 100)]  # 创建clip轮廓，长方形
    pp1, pp2, pp3, pp4, pp5 = Point3D(0, 0, 0), Point3D(100, 0, 0), Point3D(100, 100, 0), Point3D(0, 100, 0), Point3D(0,
                                                                                                                      0,
                                                                                                                      0)
    outerPoly = [pp1, pp2, pp3, pp4, pp5]  # 外轮廓，逆时针
    pp1, pp2, pp3, pp4, pp5 = Point3D(30, 30, 0), Point3D(30, 70, 0), Point3D(70, 70, 0), Point3D(70, 30, 0), Point3D(
        30, 30, 0)
    innerPoly = [pp1, pp2, pp3, pp4, pp5]  # 内轮廓，顺时针
    # print(innerPoly)
    p1 = Polyline()
    p1.add_head(outerPoly)
    p2 = Polyline()
    p2.add_head(innerPoly)
    p = genCpPath([p1, p2], 15, 30)
    for i in range(len(p.paths)):
        for j in range(p[i].count()):
            print(p[i].points[j])
'''
