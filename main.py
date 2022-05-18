from GenSptPath import *
from GenCpPath import *

# 整体展示
stlModel = StlModel()
layerThk = 20.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm 20
path = "./STL/monk.stl"
src = stlModel.readStlFile(path)
stlModel.getBounds()
slicem = SliceModel(stlModel, layerThk, 'optimal')
angle = 0  # 设置填充角度，单位：度
interval = 0.5  # 轮廓路径间距
shellThk = 2.0  # 外壳厚度，即轮廓路径总宽度
layers = slicem.layers  # 读取相应切片文件
for i in range(len(layers)):  # 遍历各切片层轮廓
    print('dp,layer:%d/%d' % (i + 1, len(layers)))  # 打印当前切片层信息
    slicem.layers[i].contours = LinkSegs_dlook(slicem.layers[i].segments).contours
    theta = degToRad(angle) if (i % 2 == 1) else degToRad(angle + 90)  # 正交填充角度
    if len(layers[i].contours) == 0:
        continue
    gcp = genCpPath(layers[i].contours, interval, shellThk)
    layers[i].cpaths = gcp.paths
    layers[i].dpaths = genDpPath(gcp.inpolys, interval, theta)  # 生成平行路径
genSptPath(stlModel, layers, 2, 2, degToRad(60))  #支撑区域

va = VtkAdaptor()  # 以下调用VTK显示计算结果
va.drawPdSrc(src).GetProperty().SetOpacity(0.1)  # 显示三维模型
for layer in layers:  # 逐层显示填充路径
    for poly in layer.sptDpPaths:  # 显示平行填充路径
        if poly is not None:
            va.drawPolyline(poly).GetProperty().SetColor(1, 0, 0)  # 平行路径红色
    for poly in layer.sptCpPaths:  # 显示轮廓路径
        if poly is not None:
            va.drawPolyline(poly).GetProperty().SetColor(0, 0, 1)  # 轮廓路径蓝色
    for poly in layer.dpaths:
        if poly is not None:
            va.drawPolyline(poly).GetProperty().SetColor(0, 0, 0)
    for poly in layer.cpaths:
        if poly is not None:
            va.drawPolyline(poly).GetProperty().SetColor(0, 1, 0)
va.display()
