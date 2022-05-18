import SliceAlgo
import vtk
from GeomAIgo import *
from IntersectStl_sweep import *
from STL import *
from VtkAdaptor import *


# 主要功能是将对 StlModel 进行转化，并通过类内的切片函数对模型进行切片。最终将得到的不同高度的切片对象 Layer，保存在self.layers 中


class SliceModel:
    def __init__(self, stlModel, layerThk, sliceAlgo):  # 初始化函数，输入模型、
        self.stlModel = stlModel  # 层高以及切片方式
        self.layerThk = layerThk
        if sliceAlgo == 'brutal':
            self.slice_brutal()
        elif sliceAlgo == 'optimal':
            self.slice_sweep()
        elif sliceAlgo == 'optimal2':
            self.slice_sweep()

    def slice_brutal(self):  # 切片函数，brutal
        self.layers = SliceAlgo.intersectStl_brutal(self.stlModel, self.layerThk)
        # for layer in self.layers:
        # layer.contours=SliceAlgo.linkSegs_brutal(layer.segments)
        # SliceAlgo.adjustPolygonDirs(layer.contours)

    def slice_sweep(self):  # 切片函数，优化扫描
        self.layers = SliceAlgo.intersectStl_sweep(self.stlModel, self.layerThk)

    def slice_height(self):  # 切片函数，优化层高
            self.layers = SliceAlgo.intersectStl_sweep(self.stlModel, self.layerThk)

    def adjust_direction(self):
        for layer in self.layers:
            adjustPolygonDirs(layer.contours)

    def writeSlcFile(self, path):  # 写SLC文件
        SliceAlgo.writeSlcFile(self.layers, path)

    def readSlcFile(self, path):  # 读SLC文件
        self.layers = SliceAlgo.readSlcFile(path)

    def drawLayerContours(self, va, start=0, stop=0xFFFF, step=1, clr=(0, 0, 0), lineWidth=1):
        pass


if __name__ == '__main__':  # SliceModel类测试
    import time
    stlModel = StlModel()
    stlModel.readStlFile("./STL/bunny.STL")  # 读取STL文件
    start = time.time()
    sliceModel = SliceModel(stlModel, 1.0, 'optimal')  # 建立切片模型，输入层高mm
    # sliceModel = SliceModel(stlModel, 1.0, 'brutal')  # 建立切片模型，输入层高mm
    #sliceModel = SliceModel(stlModel, 1.0, 'optimal2')  # 建立切片模型，输入层高mm
    end = time.time()
    print(end - start)
