from GeomAIgo import *
import Utility


# 封装一个用于确定多边形父子关系的类，用于轮廓填充
class PolyPcrSeeker:  # 定义PolyPcrSeeker类
    def __init__(self, polys):  # 初始化函数，输入曲线列表
        self.polys = Utility.makeListLinear(polys)  # 转化输入列表为线性列表
        self.seek()  # 调用类核心函数

    def seek(self):  # 定义寻找父子关系的核心函数
        polys = self.polys  # 仅仅是方便书写
        for poly in polys:  # 遍历输入polys
            poly.area = math.fabs(poly.getArea())  # 动态定义曲线面积属性
            poly.parent = None  # 动态定义曲线的父曲线属性
            poly.childs = []  # 动态定义曲线的子曲线属性
            poly.depth = 0  # 动态定义曲线的深度属性
        polys.sort(key=lambda t: t.area)  # 根据面积对曲线排序
        for i in range(len(polys) - 1):  # 第1重循环，i从0开始
            pt = polys[i].startPoint()  # 取第1条曲线的起点为测试点
            for j in range(i + 1, len(polys)):  # 第2重循环，j从i+1开始
                if pointInPolygon(pt, polys[j]) == 1:  # 测试点是否在第2条曲线内部
                    polys[i].parent = polys[j]  # 指定父曲线
                    polys[j].childs.append(polys[i])  # 添加子曲线
                    break  # 退出第二重循环
        for poly in polys:  # 遍历polys，计算每条曲线深度值
            self.findPolyDepth(poly)
        polys.sort(key=lambda t: t.depth)  # 依据曲线深度值对polys排序

    def findPolyDepth(self, poly):  # 定义曲线深度值计算函数
        crtPoly = poly
        while crtPoly.parent is not None:  # 如果当前曲线的父曲线不为空
            crtPoly = crtPoly.parent  # 则令当前曲线为父曲线
            poly.depth += 1  # 并自增原曲线的深度值


def seekPolyPcr(polys):  # 定义类使用的全局接口函数
    return PolyPcrSeeker(polys).polys
