from SliceAlgo import *
import vtk
from STL import *

path = "./STL/monk.stl"
layerThk = 10.0  # 指定切片厚度：2.0,1.0,0.5,0.2mm

stlModel = StlModel()
stlModel.readStlFile(path)
stlModel.getBounds()
slicem = SliceModel(stlModel, layerThk, 'optimal')
layers = slicem.layers  # 使用拓扑切片获取每层轮廓数据
