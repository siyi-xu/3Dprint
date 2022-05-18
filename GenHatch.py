from GeomAIgo import *


# 实现对于输入轮廓和平行扫描线列表，得到其截交线段，并将截
# 交线段 Z 字形连接，输出为对应的方向填充路径
class SweepLine:  # 定义SweepLine类，扫描线
    def __init__(self):
        self.segs = []  # 属性segs，Segment类型列表

    def intersect(self, y):  # 定义segs和y线的求交函数
        ips = []  # 交点列表
        yLine = Line(Point3D(0, y, self.segs[0].A.z), Vector3D(1, 0, 0))  # 创建和X轴平行的y线
        for seg in self.segs:  # 遍历segs，和y线求交
            if seg.A.y == y:  # 重要：如果y线经过线段A端点
                ips.append(seg.A.clone())  # 则将A端点添加至交点列表
            elif seg.B.y == y:  # 同理，如果y线经过线段B端点
                ips.append(seg.B.clone())  # 则将B端点添加至交点列表
            else:  # 否则，使用intersect函数计算y
                ip = intersect(yLine, seg)  # 线和线段交点，并将交点添加至
                if ip is not None:  # 交点列表，ip：intersectionpoint
                    ips.append(ip)
        ips.sort(key=lambda p: p.x)  # 对交点按x值从小到大排序

        i = len(ips) - 1
        while i > 0:  # 移除交点列表中的重合点对
            if ips[i].distanceSquare(ips[i - 1]) == 0:  # 逐个比较相邻点是否重合
                del ips[i]
                del ips[i - 1]
                i = i - 2  # 如果点对被移除，i向前走2步
            else:  # 否则i向前走1步
                i = i - 1
        return ips  # 返回处理后的交点列表


def calcHatchPoints(polygons, ys):  # 输入多边形和扫描高度ys
    segs = []  # 存放多边形边的线段列表
    for poly in polygons:  # 遍历多边形，收集所有线段
        for i in range(poly.count() - 1):
            seg = Segment(poly.points[i], poly.points[i + 1])  # 根据多边形相邻顶点创建线段
            seg.yMin = min(seg.A.y, seg.B.y)  # 计算并保存线段最低点y值yMin
            seg.yMax = max(seg.A.y, seg.B.y)  # 计算并保存线段最高点y值yMax
            segs.append(seg)
    segs.sort(key=lambda s: s.yMin)  # 根据最低点y值对线段升序排序

    k, sweep = 0, SweepLine()  # 创建扫描线对象
    ipses = []  # 交点列表
    for y in ys:  # 遍历扫描线高度
        for i in range(len(sweep.segs) - 1, -1, -1):  # 移除不再和扫描线相交的线段
            if sweep.segs[i].yMax < y:
                del sweep.segs[i]

        for i in range(k, len(segs)):  # 从segs添加和扫描线相交的线段
            if segs[i].yMin < y and segs[i].yMax >= y:  # 将满足最低点小于y，最高点大于
                sweep.segs.append(segs[i])  # 等于y的线段添加至扫描线
                if i == len(segs) - 1:
                    k = len(segs)

            elif segs[i].yMin >= y:  # 知道线段最低点大于等于y值，
                k = i  # 停止添加线段，并记录k值
                break
        if len(sweep.segs) > 0:  # 如果扫描线中线段数量不为0，
            ips = sweep.intersect(y)  # 则调用SweepLine的intersect
            ipses.append(ips)  # 函数计算扫描线和线段交点
    return ipses  # 返回得到的二维交点列表


def genSweepHatches(polygons, interval, angle):  # 定义均匀填充线生成函数
    mt = Matrix3D.createRotateMatrix('Z', -angle)  # 旋转矩阵，matrixto，去
    mb = Matrix3D.createRotateMatrix('Z', angle)  # 旋转矩阵，matrixback，回
    rotPolys = []  # 存储旋转后多边形
    for poly in polygons:  # 遍历，旋转多边形，作用mt
        rotPolys.append(poly.multiplied(mt))
    yMin, yMax = float('inf'), float('-inf')  # 获取旋转后多边形最低和最高值
    for poly in rotPolys:
        for pt in poly.points:
            yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
    ys = []  # 存储扫描线高度
    y = yMin + interval  # 其实高度
    while y < yMax:  # 根据输入间距生成高度列表ys
        ys.append(y)
        y += interval
    segs = genHatches(rotPolys, ys)  # 对旋转多边形生成填充线段
    for seg in segs:  # 遍历，旋转填充线段，作用mb
        seg.multiply(mb)
    return segs  # 最后返回旋转后的填充线列表


def genHatches(polygons, ys):  # 填充线生成函数，不涉及旋转
    segs = []
    ipses = calcHatchPoints(polygons, ys)  # 生成填充线交点，二维列表
    for ips in ipses:  # 根据填充线奇偶提取原则从交点
        for i in range(0, len(ips) - 1, 2):  # 列表中提取填充线
            seg = Segment(ips[i], ips[i + 1])
            segs.append(seg)
    return segs  # 返回填充线段，一维列表


def linkLocalHatches(segs):
    result = Polyline()
    flag = 0
    for i in range(len(segs)):
        if flag == 0:
            result.addPoint(segs[i].A)
            segs[i].B.w = 1
            result.addPoint(segs[i].B)
            flag = 1
        else:
            result.addPoint(segs[i].B)
            segs[i].A.w = 1
            result.addPoint(segs[i].A)
            flag = 0
    return result
