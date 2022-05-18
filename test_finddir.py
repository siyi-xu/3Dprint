from FindOptFeedDir import *
import time
from SliceModel import *
from GenDpPath import *
from STL import *


# 方向填充角度优化
def getAngleTable(polygons):  # 角度表
    start = time.time()
    angleTable = findOptFeedDir(polygons, 0)
    for key in angleTable.keys():
        print(key, angleTable[key])
    end = time.time()
    print("getAngleTabletime:%fCPUseconds\n" % (end - start))


def getRegionTable(polygons):  # 暴力方法计算分区表,作为getAngletable的对比
    start = time.time()
    regionTable = {}
    for angle in range(0, 180, 1):
        rotPolys = rotatePolygons(polygons, -degToRad(angle))  # 对轮廓旋转，反向
        splitPolys = splitRegion(rotPolys)
        regionTable[angle] = len(splitPolys)
    for key in regionTable.keys():
        print(key, regionTable[key])
    end = time.time()
    print("getRegionTabletime:%fCPUseconds\n" % (end - start))


def getPathCount(polygons, interval):  # 生成轮廓区域内的实际平行填充路径，并统计路径数量
    min_angle = 0
    min_path = []
    for angle in range(0, 180, 1):
        paths = genDpPath(polygons, interval, degToRad(angle))
        if angle == 0:
            min_path = paths
        print(len(paths))
        if len(paths) < len(min_path):
            min_angle = angle
            min_path = paths
    print("min_angle:", min_angle)
    return min_angle, min_path


if __name__ == '__main__':  # 跳刀优化测试：输入切片轮廓，计算、打印角度表
    path = "./STL/monk.stl"
    interval = 3  # 设置填充路径间距
    angle = 0  # 设置填充角度，单位：度
    pathses = []  # 存放各切片层平行路径

    layerThk = 10.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm
    stlModel = StlModel()
    stlModel.readStlFile(path)
    stlModel.getBounds()
    slicem = SliceModel(stlModel, layerThk, 'optimal')

    layers = slicem.layers
    layer = layers[3]
    layer.contours = LinkSegs_dlook(layer.segments).contours
    getAngleTable(layer.contours)
    getRegionTable(layer.contours)
    getPathCount(layer.contours, 0.1)
