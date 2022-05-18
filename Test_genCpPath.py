from GenCpPath import *
import time
from STL import *
from LinkSegs_dlook import *
from VtkAdaptor import *

interval = 0.2  # 轮廓路径间距 monk0.4 2
shellThk = 1.0  # 外壳厚度，即轮廓路径总宽度
pathses = []  # 存储各层已连接的路径
layerThk = 1.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm
path = "./STL/bunny.STL"
stlModel = StlModel()
stlModel.readStlFile(path)
stlModel.getBounds()
slicem = SliceModel(stlModel, layerThk, 'optimal')

len_l = len(slicem.layers)  # 使用拓扑切片获取每层轮廓数据

start = time.time()  # 计时开始
for i in range(len_l):  # 逐层生成轮廓填充路径
    print('cp,layer:%d/%d' % (i + 1, len_l))
    slicem.layers[i].contours = LinkSegs_dlook(slicem.layers[i].segments).contours

slicem.adjust_direction()
for i in range(len_l):
    l = len(slicem.layers[i].contours)
    #print(l)
    if l == 0:
        continue
    paths = genCpPath(slicem.layers[i].contours, interval, shellThk).paths
    pathses.append(paths)  # 存储路径到pathses
end = time.time()
print("轮廓平行路径生成时间：", end - start)  # 打印路径生成时间
va = VtkAdaptor()  # 显示，使用VTK库
for layer in slicem.layers:  # 显示每层打印区域边界，黑色
    for contour in layer.contours:
        va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
for paths in pathses:  # 显示每层路径，红色
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1, 0, 0)
va.display()
