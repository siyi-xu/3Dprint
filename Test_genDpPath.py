from GenDpPath import *#导入GenDpPath模块
import time
from Utility import *
from STL import *
interval = 1  # 设置填充路径间距 monk3
angle = 0  # 设置填充角度，单位：度
pathses = []  # 存放各切片层平行路径
layerThk = 1.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm
path = "./STL/bunny.stl"
stlModel=StlModel()
stlModel.readStlFile(path)
stlModel.getBounds()
slicem = SliceModel(stlModel,layerThk,'optimal')
layers = slicem.layers
start = time.time()  # 计时开始
for i in range(len(layers)):  # 遍历各切片层轮廓
    print('dp,layer:%d/%d'%(i+1,len(layers)))  # 打印当前切片层信息
    slicem.layers[i].contours = LinkSegs_dlook(slicem.layers[i].segments).contours
    theta = degToRad(angle) if(i%2 == 1) else degToRad(angle+90)  # 正交填充角度
    paths = genDpPath(layers[i].contours, interval, theta)  # 生成平行路径
    pathses.append(paths)
# for i in range(len(pathses)):
#     print(pathses[i])
end = time.time()  # 计时结束
print("方向平行路径生成时间：", end - start)  # 打印平行路径生成所需时间
va = VtkAdaptor()  # 调用VTK绘图
for layer in layers:  # 绘制切片轮廓，黑色
    for contour in layer.contours:
        va.drawPolyline(contour).GetProperty().SetColor(0,0,0)
for paths in pathses:  # 绘制平行填充路径，红色
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1,0,0)
va.display()
