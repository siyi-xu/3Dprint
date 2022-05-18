from GenDpPath import *
from FindSptRegion import *


# 支撑带填充
def genSptPath(stlModel, Layers, pathInvl, gridSize, crAngle, fillType="line", fillAngle=0, xyGap=1):
    for i in range(len(Layers)):  # 遍历各切片层轮廓
        print('dp,layer:%d/%d' % (i + 1, len(Layers)))  # 打印当前切片层信息
        Layers[i].contours = LinkSegs_dlook(Layers[i].segments).contours
        adjustPolygonDirs(Layers[i].contours)
    ys = findSptRegion(stlModel, Layers, gridSize, crAngle, xyGap)  # 寻找支撑区域
    for i in range(len(Layers)):
        Layers[i].sptDpPaths = genDpPathEx(Layers[i].sptContours, pathInvl, fillAngle, ys)
        Layers[i].sptCpPaths = Layers[i].sptContours


if __name__ == '__main__':
    stlModel = StlModel()
    layerThk = 10.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm
    path = "./STL/monk.stl"
    src = stlModel.readStlFile(path)
    stlModel.getBounds()
    slicem = SliceModel(stlModel, layerThk, 'optimal')

    layers = slicem.layers  # 读取相应切片文件
    genSptPath(stlModel, layers, 2, 2, degToRad(60))
    va = VtkAdaptor()  # 以下调用VTK显示计算结果
    va.drawPdSrc(src).GetProperty().SetOpacity(0.1)  # 显示三维模型
    for layer in layers:  # 逐层显示填充路径
        for poly in layer.sptDpPaths:  # 显示平行填充路径
            if poly is not None:
                va.drawPolyline(poly).GetProperty().SetColor(1, 0, 0)  # 平行路径红色
        for poly in layer.sptCpPaths:  # 显示轮廓路径
            if poly is not None:
                va.drawPolyline(poly).GetProperty().SetColor(0, 0, 1)  # 轮廓路径蓝色
    va.display()
