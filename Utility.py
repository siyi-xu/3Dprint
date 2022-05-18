import math


def makeListLinear(lists):  # 定义makeListLinear函数，功能
    outList = []  # 是将多维列表转化为一维列表
    _makeListLinear(lists, outList)
    return outList


def _makeListLinear(inList, outList):  # 定义makeListLinear依赖函数
    for a in inList:  # 这个函数通过递归的方法将多维
        if type(a) != list:  # 列表转化为一维列表
            outList.append(a)  # 注意：我们一般不会在外部调用带
        else:  # 下划线的函数
            _makeListLinear(a, outList)


def degToRad(deg):  # 角度转化为弧度
    return deg * math.pi / 180.0


def radToDeg(rad):  # 弧度转化为角度
    return rad * 180.0 / math.pi
