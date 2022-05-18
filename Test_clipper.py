from pyclipper import *  # 导入pyclipper模块
from VtkAdaptor import *  # 导入可视化模块
from Polyline import *
from GeomBase import *
from GenCpPath import *
from PolyPcrSeeker import *


def tuplesToPoly(tuples):  # 定义将元组序列转化为Polyline函数
    poly = Polyline()
    for pt in tuples: poly.addPoint(Point3D(pt[0], pt[1], 0))  # 多边形z坐标始终为0
    poly.addPoint(poly.startPoint())
    return poly


if __name__ == '__main__':  # 测试main函数入口
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
    p = seekPolyPcr([p2, p1])
    print(p[1].parent)
    '''
    pco=PyclipperOffset()#创建PyClipperOffset对象pco
    pco.AddPath(outerPoly,JT_ROUND,ET_CLOSEDPOLYGON)#添加外轮廓
    pco.AddPath(innerPoly,JT_ROUND,ET_CLOSEDPOLYGON)#添加内轮廓
    sln=pco.Execute(-7)
    vtkAdaptor=VtkAdaptor()#定义可视化对象
    for tuples in sln:#转换轮廓数据格式并显示
        poly=tuplesToPoly(tuples)
        print(poly)
        vtkAdaptor.drawPolyline(poly).GetProperty().SetColor(0,0,0)
    vtkAdaptor.display()
    '''
