from LinkPoint import *
from Polyline import *
from SliceModel import *


# 将输入的线段拼接,字典查询法

class LinkSegs_dlook:  # 类定义
    def __init__(self, segs):  # 初始化函数，输入线段列表segs
        self.segs = segs  # 保存线段列表
        self.contours = []  # 保存封闭轮廓
        self.polys = []  # 保存非封闭轮廓
        self.link()  # 调用拼接函数

    def link(self):  # 字典查询法拼接函数，略
        dic = self.createLpDic()
        p = self.findUnusedPnt(dic)
        while p != None:
            contour = Polyline()
            contour.addPoint(p.toPoint3D())
            while contour.isclose() == False:
                p.used = True
                p.other.used = True
                nextp = self.findNextPnt(p, dic)
                if nextp == None:
                    self.polys.append(contour)
                    break
                p = nextp
                contour.addPoint(p.toPoint3D())
            if contour.isclose():
                self.contours.append(contour)
            p = self.findUnusedPnt(dic)

    def createLpDic(self):  # 构建字典函数
        dic = {}  # 字典初始化
        for seg in self.segs:  # 遍历segs
            lp1, lp2 = LinkPoint(seg.A), LinkPoint(seg.B)  # 构建两个LinkPoint数据点
            lp1.other, lp2.other = lp2, lp1  # 点的other属性相互赋值
            if (lp1.x, lp1.y) not in dic.keys():  # 判断lp1坐标是否在字典的键中
                dic[(lp1.x, lp1.y)] = []  # 如果不在则对该键新建列表
                dic[(lp1.x, lp1.y)].append(lp1)
            if len(dic[(lp1.x, lp1.y)]) == 1 and dic[(lp1.x, lp1.y)][0] != lp1:
                dic[(lp1.x, lp1.y)].append(lp1)
            if (lp2.x, lp2.y) not in dic.keys():  # 对lp2执行相同的操作
                dic[(lp2.x, lp2.y)] = []
                dic[(lp2.x, lp2.y)].append(lp2)
            if len(dic[(lp2.x, lp2.y)]) == 1 and dic[(lp2.x, lp2.y)][0] != lp2:
                dic[(lp2.x, lp2.y)].append(lp2)
        return dic  # 返回字典

    def findUnusedPnt(self, dic):
        for i in dic:
            for j in dic[i]:
                if j.used == False:
                    return j
        return None

    def findNextPnt(self, p, dic):
        key = (p.other.x, p.other.y)
        if key not in dic:
            return None
        list = dic[key]
        if len(list) > 2:
            return None
        for i in list:
            if i == p.other:
                continue
            else:
                return i
        return None


if __name__ == "__main__":  # 展示截交拼接时间
    import time
    path = "./STL/bunny.stl"
    stlm = StlModel()
    vtkStlReader = stlm.readStlFile(path)
    start = time.time()
    slicem = SliceModel(stlm, 1, 'optimal')
    print("截交时间：", time.time() - start)
    start = time.time()
    for i in range(len(slicem.layers)):
        ld = LinkSegs_dlook(slicem.layers[i].segments)  # 拼接
    print("拼接时间：", time.time() - start)
