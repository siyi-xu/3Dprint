from GeomBase import *
from Line import *
from Ray import *
from Segment import *
from Plane import *
from Polyline import *


# 求取空间三角形和z平面的交线

def nearZero(x):  # 判断某一个数是否接近0
    return True if math.fabs(x) < epsilon else False  # 判断该数和给定极小数的关系


def distance(obj1, obj2):  # 实体距离计算
    if isinstance(obj1, Point3D) and isinstance(obj2, Line):  # 情况1: 点和直线距离计算
        P, Q, V = obj2.P, obj1, obj2.V
        t = P.pointTo(Q).dotProduct(V)
        R = P + V.amplified(t)
        return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Ray):  # 情况2: 点和射线距离计算
        P, Q, V = obj2.P, obj1, obj2.V
        t = P.pointTo(Q).dotProduct(V)
        if t >= 0:
            R = P + V.amplified(t)
            return Q.distance(R)
        return Q.distance(P)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Segment):  # 情况3: 点和直线距离计算
        Q, P, P1, V = obj1, obj2.A, obj2.B, obj2.direction().normalized()
        L = obj2.length()
        t = P.pointTo(Q).dotProduct(V)
        if t <= 0:
            return Q.distance(P)
        elif t >= L:
            return Q.distance(P1)
        else:
            R = P + V.amplified(t)
            return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Plane):  # 情况4:点和直线距离计算
        P, Q, N = obj2.P, obj1, obj2.N
        angle = N.getAngle(P.pointTo(Q))
        return P.distance(Q) * math.cos(angle)
    elif isinstance(obj1, Line) and isinstance(obj2, Line):  # 情况5:直线和直线距离计算
        P1, V1, P2, V2 = obj2.P, obj1.V, obj2.P, obj2.V
        N = V1.crossProduct(V2)
        if N.isZeroVector():
            return distance(P1, obj2)
        return distance(P1, Plane(P2, N))
    elif isinstance(obj1, Line) and isinstance(obj2, Plane):  # 情况6: 直线和平面距离计算
        if obj1.V.dotProduct(obj2.N) == 0:
            return distance(obj1.P, obj2)
        else:
            return 0


def intersectLineLine(line1: Line, line2: Line):  # 计算直线和直线的交点
    P1, V1, P2, V2 = line1.P, line1.V, line2.P, line2.V
    P1P2 = P1.pointTo(P2)
    deno = V1.dy * V2.dx - V1.dx * V2.dy  # 分母
    if deno != 0:
        t1 = -(-P1P2.dy * V2.dx + P1P2.dx * V2.dy) / deno
        t2 = -(-P1P2.dy * V1.dx + P1P2.dx * V1.dy) / deno
        return P1 + V1.amplified(t1), t1, t2
    else:
        deno = V1.dz * V2.dy - V1.dy * V2.dz
        if deno != 0:
            t1 = -(-P1P2.dz * V2.dy + P1P2.dy * V2.dz) / deno
            t2 = -(-P1P2.dz * V1.dy + P1P2.dy * V1.dz) / deno
            return P1 + V1.amplified(t1), t1, t2
    return None, 0, 0  # 如果不相交,返回None


def intersectSegmentPlane(seg: Segment, plane: Plane):  # 计算线段和平面交点
    A, B, P, N = seg.A, seg.B, plane.P, plane.N
    V = A.pointTo(B)
    PA = P.pointTo(A)
    if V.dotProduct(N) == 0:
        return None  # 线段和平面平行,返回None
    else:
        t = -(PA.dotProduct(N) / V.dotProduct(N))
        if 0 <= t <= 1:
            return A + (V.amplified(t))
    return None


def intersectTrianglePlane(triangle, plane):
    AB = Segment(triangle.A, triangle.B)
    AC = Segment(triangle.A, triangle.C)
    BC = Segment(triangle.B, triangle.C)
    c1 = intersectSegmentPlane(AB, plane)  # 3条边和平面交点
    c2 = intersectSegmentPlane(AC, plane)
    c3 = intersectSegmentPlane(BC, plane)
    if c1 is None:  # 分类讨论，枚举各种情况
        if c2 is not None and c3 is not None:  # 存在2个交点的情况
            if c2.distance(c3) != 0.0:
                return Segment(c2, c3)
    elif c2 is None:
        if c1 is not None and c3 is not None:  # 存在2个交点的情况
            if c1.distance(c3) != 0.0:
                return Segment(c1, c3)
    elif c3 is None:
        if c1 is not None and c2 is not None:  # 存在2个交点的情况
            if c1.distance(c2) != 0.0:
                return Segment(c1, c2)
    elif c1 is not None and c2 is not None and c3 is not None:  # 存在3个交点的情况
        return Segment(c1, c3) if c1.isIdentical(c2) else Segment(c1, c2)
    return None  # 如果都不满足，返回None


def intersectTriangleZPlane(triangle, z):
    if triangle.zMinPnt() > z:
        return None
    if triangle.zMaxPnt() < z:
        return None
    return intersectTrianglePlane(triangle, Plane.zPlane(z))


def intersect(obj1, obj2):  # 实体求交计算
    if isinstance(obj1, Line) and isinstance(obj2, Line):  # 情况1:直线和直线求交
        P, t1, t2 = intersectLineLine(obj1, obj2)
        return P
    elif isinstance(obj1, Segment) and isinstance(obj2, Segment):  # 情况2:线段和线段求交
        line1, line2 = Line(obj1.A, obj1.direction()), Line(obj2.A, obj2.direction())
        P, t1, t2 = intersectLineLine(line1, line2)  # 调用intersectLineLine函数
        if P is not None:
            if 0 <= t1 <= obj1.length() and 0 <= t2 <= obj2.length():
                return P
        return None
    elif isinstance(obj1, Line) and isinstance(obj2, Segment):  # 情况3:直线和线段求交
        line1, line2 = obj1, Line(obj2.A, obj2.direction())
        P, t1, t2 = intersectLineLine(line1, line2)
        return P if P is not None and 0 <= t2 <= obj2.length() else None
    # 4.直线和射线求交, 5.射线和线段求交, 6.射线和射线求交 略
    elif isinstance(obj1, Line) and isinstance(obj2, Plane):  # 情况7:直线和平面求交
        P0, V, P1, N = obj1.P, obj1.V, obj2.P, obj2.N
        dotPro = V.dotProduct(N)
        if dotPro != 0:
            t = P0.pointTo(P1).dotProduct(N) / dotPro
            return P0 + V.amplified(t)
        return None
    # 8.射线和平面相交
    elif isinstance(obj1, Segment) and isinstance(obj2, Plane):  # 情况9:线段和平面相交
        return intersectSegmentPlane(obj1, obj2)
    pass  # 实体求交有待扩展


def pointOnRay(p: Point3D, ray: Ray):  # 判断点是否在射线上
    v = ray.P.pointTo(p)
    return True if v.dotProduct(ray.V) >= 0 and v.crossProduct(ray.V).isZeroVector() else False


def pointInPolygon(p: Point3D, polygon: Polyline):  # 判断点是否在多边形内部
    passCount = 0  # 返回1:点在多边形内部
    ray = Ray(p, Vector3D(1, 0, 0))  # 返回0:点在多边形外部
    segments = []  # 返回-1,点在多边形上
    for i in range(polygon.count() - 1):
        seg = Segment(polygon.points[i], polygon.points[i + 1])
        segments.append(seg)
    for seg in segments:  # 计算线段(不包含端点)和射线交点个数
        line1, line2 = Line(ray.P, ray.V), Line(seg.A, seg.direction())
        P, t1, t2 = intersectLineLine(line1, line2)

        if P is not None:
            if nearZero(t1):
                return -1
            elif seg.A.y != p.y and seg.B.y != p.y and t1 > 0 and 0 < t2 < seg.length():
                passCount += 1
    upSegments, downSegments = [], []  # 存放射线上方和下方的线段
    for seg in segments:
        if seg.A.isIdentical(ray.P) or seg.B.isIdentical(ray.P):
            return -1  # 点在多边形边上
        elif pointOnRay(seg.A, ray) ^ pointOnRay(seg.B, ray):
            if seg.A.y >= p.y and seg.B.y >= p.y:
                upSegments.append(seg)
            elif seg.A.y <= p.y and seg.B.y <= p.y:
                downSegments.append(seg)

    passCount += min(len(upSegments), len(downSegments))  # 顶点配对

    if passCount % 2 == 1:  # 射线穿过多边形次数为奇数,
        return 1  # 则点在多边形内部
    return 0  # 否则点在多边形外部


def adjustPolygonDirs(polygons):  # 输入为轮廓列表
    for i in range(len(polygons)):  # 第1个循环
        pt = polygons[i].startPoint()  # 取出待检测轮廓上的起点
        insideCount = 0  # 点在几个多边形内部计数
        for j in range(len(polygons)):  # 第2个循环
            if j == i: continue  # 如果两个多边形一样则跳过
            restPoly = polygons[j]
            if 1 == pointInPolygon(pt, restPoly):  # 点在另一多边形内部，则加1
                insideCount += 1
        if insideCount % 2 == 0:  # 判断点在内部次数是否为偶数
            d = polygons[i].makeCCW()  # 调整多边形方向为逆时针
        else:
            d = polygons[i].makeCW()  # 调整多边形方向为顺时针


def rotatePolygons(polygons, angle, center=None):  # 定义旋转多边形函数
    dx = 0 if center is None else center.x  # 旋转中心X坐标，默认为0
    dy = 0 if center is None else center.y  # 旋转中心Y坐标，默认为0
    mt = Matrix3D.createTranslateMatrix(-dx, -dy, 0)  # 构造平移矩阵，matrixto
    mr = Matrix3D.createRotateMatrix('Z', angle)  # 构造旋转矩阵，旋转轴为Z轴
    mb = Matrix3D.createTranslateMatrix(dx, dy, 0)  # 构造反向平移矩阵，matrixback
    m = mt * mr * mb  # 变换矩阵乘积
    newPolys = []

    for poly in polygons:  # 遍历，对每个多边形变换
        newPolys.append(poly.multiplied(m))
    return newPolys  # 返回变换后矩阵序列
