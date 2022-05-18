import math

# 帮助STL中的Triangle类实现
epsilon = 1e-7
epsilonSquare = epsilon * epsilon


class Point3D:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x, self.y, self.z, self.w = x, y, z, w

    def __str__(self):
        return "Point3D:%s,%s,%s" % (self.x, self.y, self.z)

    def clone(self):
        return Point3D(self.x, self.y, self.z, self.w)

    def pointTo(self, other):
        return Vector3D(other.x - self.x, other.y - self.y, other.z - self.z)

    def translate(self, vec):  # 根据向量对当前点进行平移
        self.x = self.x + vec.dx
        self.y = self.y + vec.dy
        self.z = self.z + vec.dz

    def translated(self, vec):  # 对当前点进行平移后返回新点
        return Point3D(self.x + vec.dx, self.y + vec.dy, self.z + vec.dz)

    def multiplied(self, m):  # 点右乘一个矩阵后返回新点
        x = self.x * m.a[0][0] + self.y * m.a[1][0] + self.z * m.a[2][0] + self.w * m.a[3][0]
        y = self.x * m.a[0][1] + self.y * m.a[1][1] + self.z * m.a[2][1] + self.w * m.a[3][1]
        z = self.x * m.a[0][2] + self.y * m.a[1][2] + self.z * m.a[2][2] + self.w * m.a[3][2]
        return Point3D(x, y, z)

    def distance(self, other):  # 计算两点之间的距离
        return self.pointTo(other).length()

    def distanceSquare(self, other):  # 计算两点之间距离的平方
        return self.pointTo(other).lengthSquare()

    def middle(self, other):  # 计算两个点的中点
        return Point3D((self.x + other.x) / 2, (self.y + other.y) / 2, (self.z + other.z) / 2)

    def isCoincide(self, other, dis2=epsilonSquare):  # 根据两点之间的距离判断两点是否重合
        return True if self.pointTo(other).lengthSquare() < dis2 else False

    def isIdentical(self, other):  # 判断两点之间是否重合
        return True if self.x == other.x and self.y == other.y and self.z == other.z else False

    def __add__(self, vec):
        return self.translated(vec)

    def __sub__(self, other):
        return other.pointTo(self) if isinstance(other, Point3D) else self.translated(other.reversed())

    def __mul__(self, m):
        return self.multiplied(m)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False


class Vector3D:
    def __init__(self, dx=0.0, dy=0.0, dz=0.0, dw=0.0):
        self.dx, self.dy, self.dz, self.dw = dx, dy, dz, dw

    def __str__(self):
        return "Vector3D:%s,%s,%s" % (self.dx, self.dy, self.dz)

    def clone(self):
        return Vector3D(self.dx, self.dy, self.dz, self.dw)

    def reverse(self):
        self.dx, self.dy, self.dz = -self.dx, -self.dy, -self.dz

    def reversed(self):
        return Vector3D(-self.dx, -self.dy, -self.dz)

    def dotProduct(self, vec):
        return self.dx * vec.dx + self.dy * vec.dy + self.dz * vec.dz

    def crossProduct(self, vec):
        dx = self.dy * vec.dz - self.dz * vec.dy
        dy = self.dz * vec.dx - self.dx * vec.dz
        dz = self.dx * vec.dy - self.dy * vec.dx
        return Vector3D(dx, dy, dz)

    def amplify(self, f):
        self.dx, self.dy, self.dz = self.dx * f, self.dy * f, self.dz * f

    def amplified(self, f):  # 对向量放大,返回新向量
        return Vector3D(self.dx * f, self.dy * f, self.dz * f)

    def lengthSquare(self):  # 向量长度的平方
        return self.dx * self.dx + self.dy * self.dy + self.dz * self.dz

    def length(self):  # 向量的长度(模)
        return math.sqrt(self.lengthSquare())

    def normalize(self):  # 对当前向量单位化
        len = self.length()
        self.dx = self.dx / len
        self.dy = self.dy / len
        self.dz = self.dz / len

    def normalized(self):  # 向量单位化,返回新向量
        len = self.length()
        return Vector3D(self.dx / len, self.dy / len, self.dz / len)

    def isZeroVector(self):  # 判断是否为零向量
        return self.lengthSquare() == 0.0

    def multiplied(self, m):  # 向量乘以矩阵
        dx = self.dx * m.a[0][0] + self.dy * m.a[1][0] + self.dz * m.a[2][0] + self.dw + m.a[3][0]
        dy = self.dx * m.a[0][1] + self.dy * m.a[1][1] + self.dz * m.a[2][1] + self.dw + m.a[3][1]
        dz = self.dx * m.a[0][2] + self.dy * m.a[1][2] + self.dz * m.a[2][2] + self.dw + m.a[3][2]
        return Vector3D(dx, dy, dz)

    def isParallel(self, other):  # 判断两个向量是否平行
        return self.crossProduct(other).isZeroVector()

    def getAngle(self, vec):  # 计算两个向量夹角,返回值0~pi
        v1 = self.normalized()
        v2 = self.normalized()
        dotPro = v1.dotProduct(v2)
        if dotPro > 1:  # 计算结果可能大于1
            dotPro = 1
        elif dotPro < -1:
            dotPro = -1
        return math.acos(dotPro)

    def getOrthoVector2D(self):  # 在XY平面上生成当前向量的正交向量
        if self.dx == 0:
            return Vector3D(1, 0, 0).normalized()
        else:
            return Vector3D(-self.dy / self.dx, 1, 0).normalized()

    def getAngle2D(self):  # 在XY平面上计算当前向量和X轴夹角
        rad = self.getAngle(Vector3D(1, 0, 0))  # 返回值0~2pi
        if self.dy < 0:
            rad = math.pi * 2.0 - rad
        return rad

    def __add__(self, other):  # 加号,两个向量相加
        return Vector3D(self.dx + other.dx, self.dy + other.dy, self.dz + other.dz)

    def __sub__(self, other):  # 减号,两个向量相减
        # return Vector3D(self.dx - other.dx, self.dy - other.dy, self.dz - other.dz)
        return self + other.reversed()

    def __mul__(self, other):  # 乘号,向量和矩阵相乘
        return self.multiplied(other)


class Matrix3D:  # 定义矩阵类
    def __init__(self):
        self.a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def __str__(self):  # 矩阵在print时的显示
        return 'Matrix3D:\n %s\n %s\n %s\n %s' % (self.a[0], self.a[1], self.a[2], self.a[3])

    def makeIdentical(self):  # 矩阵单位化
        self.a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1]]

    def multiplied(self, other):  # 当前矩阵乘以另一个矩阵
        m = Matrix3D()
        for i in range(4):
            for j in range(4):
                m.a[i][j] = self.a[i][0] * other.a[0][j] + self.a[i][1] * other.a[1][j] + self.a[i][2] * other.a[2][j] + \
                            self.a[i][3] * other.a[3][j]
        return m

    def getDeterminant(self):
        pass

    def getReverseMatrix(self):
        pass

    @staticmethod
    def createTranslateMatrix(dx, dy, dz):  # 静态函数,生成平移矩阵
        m = Matrix3D()
        m.a[3][0] = dx
        m.a[3][1] = dy
        m.a[3][2] = dz
        return m

    @staticmethod
    def createScalMatrix(sx, sy, sz):  # 静态函数,下生缩放矩阵
        m = Matrix3D()
        m.a[0][0] = sx
        m.a[0][1] = sy
        m.a[0][2] = sz
        return m

    @staticmethod
    def createRotateMatrix(axis, angle):  # 静态函数,生成旋转矩阵
        m = Matrix3D()
        sin = math.sin(angle)
        cos = math.cos(angle)
        if axis == "X" or axis == "x":
            m.a[1][1] = cos
            m.a[1][2] = sin
            m.a[2][1] = -sin
            m.a[2][2] = cos
        elif axis == "Y" or axis == "y":
            m.a[0][0] = cos
            m.a[0][2] = -sin
            m.a[2][0] = sin
            m.a[2][2] = cos
        elif axis == "Z" or axis == "z":
            m.a[0][0] = cos
            m.a[0][1] = sin
            m.a[1][0] = -sin
            m.a[1][1] = cos
        return m

    @staticmethod
    def createMirrorMatrix(point, normal):  # 静态函数,生成镜像矩阵
        pass

    def __mul__(self, other):  # 矩阵相乘,调用multiplied
        return self.multiplied(other)

    def __add__(self, other):  # 矩阵相加
        pass

    def __sub__(self, other):  # 矩阵相减
        pass
