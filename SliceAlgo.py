from IntersectStl_sweep import *
from Layer import *
import bisect
from GeomAIgo import *

# 截交的算法 实现了扫描平面的功能，通过 intersectStl_sweep，对于输入的 STL
# 模型，用扫描平面进行截交，并把截交线段存储在对应高度的 Layer 对象


# 暴力截交

def intersectStl_brutal(stlModel,layerThk):
    layers = []
    xMin, xMax, yMin, yMax, zMin, zMax = stlModel.getBounds()
    z = zMin+layerThk
    while z<zMax:
        layer = Layer(z)
        for tri in stlModel.triangles:
            seg = intersectTriangleZPlane(tri,z)
            if seg is not None:
                layer.segments.append(seg)
        layers.append(layer)
        z = z + layerThk
    return layers


# 改进的扫描法

def intersectStl_sweep(stlModel, layerThk):
    layers = []
    triangles = stlModel.triangles
    triangles.sort(key=lambda t: t.zMinPnt(), reverse=False)
    xMin, xMax, yMin, yMax, zMin, zMax = stlModel.getBounds()
    z = zMin + layerThk
    num_triangle = stlModel.getFacetNumber()
    next = 0
    swp = SweepPlane()
    while z < zMax:
        # print(z)
        for i in range(len(swp.triangles) - 1, -1, -1):
            if z > swp.triangles[i].zMaxPnt():
                del swp.triangles[i]
        for i in range(next, len(triangles)):
            tri = triangles[i]
            if z >= tri.zMinPnt() and z <= tri.zMaxPnt():
                swp.triangles.append(tri)
            elif tri.zMinPnt() > z:
                next = i
                break
        layer = Layer(z)
        for tri in swp.triangles:
            seg = intersectTriangleZPlane(tri, z)
            if seg is not None:
                layer.segments.append(seg)
        layers.append(layer)
        z = z + layerThk
    return layers


# 改进的层高法
def genLayerHeights(self): # 生成切片层高列表函数
    xMin, xMax, yMin, yMax, zMin, zMax = self.stlModel.getBounds()
    zs, layerDic = [], {} # 初始化列表，字典对象
    z = zMin + self.layerThk
    while z < zMax:
        zs.append(z) # 往列表中添加层高
        layerDic[z] = Layer(z) # 保存高度为z的层到字典中
        z += self.layerThk
    return zs, layerDic # 返回列表和字典对象

'''


def writeSlcFile(layers,path):#输入Layer列表以及文件名
    f=None
    try:
        f=open(path,'w+b')#打开（或创建）一个二进制文件
        f.write(bytes("-SLCVER2.0-UNITMM",encoding='utf-8'))#写入Header区
        f.write(bytes([0x0d,0x0a,0x1a]))#Header结尾3字节
        f.write(bytes([0x00]*256))#写入Reserved区256个0x00
        f.write(struct.pack('b',1))#写入SamplingTable区
        f.write(struct.pack('4f',0,0,0,0))
        for layer in layers:#写入ContourData区
            f.write(struct.pack('fI',layer.z,len(layer.contours)))
            for contour in layer.contours:
                f.write(struct.pack('2I',contour.count(),0))
                for pt in contour.points:
                    f.write(struct.pack('2f',pt.x,pt.y))
        f.write(struct.pack('fI',layers[-1].z,0xFFFFFFFF))#写入文件结尾
    except Exception as ex:
        print("writeSlcFile exception:",ex)#打印异常
    finally:
        if f:f.close()
'''
