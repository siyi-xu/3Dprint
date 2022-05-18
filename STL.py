from SliceModel import *
from VtkAdaptor import *
from LinkSegs_dlook import *


# STL模型加载
# STL模型三角面片的数据

class Triangle:
    def __init__(self, A, B, C, N=Vector3D(0, 0, 0)):
        self.A, self.B, self.C, self.N = A.clone(), B.clone(), C.clone(), N.clone()  # 顶点和法向self.zs=[]#存储面片包含的层高

    def __str__(self):
        pass

    def xMinPnt(self):  # 3个顶点中的X方向最低点
        return min(self.A.x, self.B.x, self.C.x)

    def xMaxPnt(self):
        return max(self.A.x, self.B.x, self.C.x)

    def yMinPnt(self):  # 3个顶点中的Y方向最低点
        return min(self.A.y, self.B.y, self.C.y)

    def yMaxPnt(self):
        return max(self.A.y, self.B.y, self.C.y)

    def zMinPnt(self):  # 3个顶点中的Z方向最低点
        return min(self.A.z, self.B.z, self.C.z)

    def zMaxPnt(self):
        return max(self.A.z, self.B.z, self.C.z)

    def calcNormal(self):
        a = ((self.B.y - self.A.y) * (self.C.z - self.A.z) - (self.B.z - self.A.z) * (self.C.y - self.A.y))
        b = ((self.B.z - self.A.z) * (self.C.x - self.A.x) - (self.B.x - self.A.x) * (self.C.z - self.A.z))
        c = ((self.B.x - self.A.x) * (self.C.y - self.A.y) - (self.B.y - self.A.y) * (self.C.x - self.A.x))
        self.N = Vector3D(a, b, c)
        self.N.normalize()


# STL模型文件读取

class StlModel:
    def __init__(self):
        self.triangles = []
        self.xMin = self.xMax = self.yMin = self.yMax = self.zMin = self.zMax = 0

    def getFacetNumber(self):
        return len(self.triangles)

    def getCoords(self, line):
        pass

    def readStlFile(self, filepath):
        stlReader = vtk.vtkSTLReader()
        stlReader.SetFileName(filepath)
        stlReader.Update()
        polydata = stlReader.GetOutput()
        cells = polydata.GetPolys()
        cells.InitTraversal()

        while True:
            idList = vtk.vtkIdList()
            res = cells.GetNextCell(idList)
            if res == 0:
                break
            pnt3ds = []
            for i in range(idList.GetNumberOfIds()):
                id = idList.GetId(i)
                x, y, z = polydata.GetPoint(id)
                pnt3ds.append(Point3D(x, y, z))
            triangle = Triangle(pnt3ds[0], pnt3ds[1], pnt3ds[2])
            triangle.calcNormal()
            self.triangles.append(triangle)
        return stlReader

    def extractFromVtkStlReader(self, vtkStlReader):
        pass

    def getBounds(self):
        self.xMin = min(self.triangles[i].xMinPnt() for i in range(self.getFacetNumber()))
        self.xMax = max(self.triangles[i].xMaxPnt() for i in range(self.getFacetNumber()))
        self.yMin = min(self.triangles[i].yMinPnt() for i in range(self.getFacetNumber()))
        self.yMax = max(self.triangles[i].yMaxPnt() for i in range(self.getFacetNumber()))
        self.zMin = min(self.triangles[i].zMinPnt() for i in range(self.getFacetNumber()))
        self.zMax = max(self.triangles[i].zMaxPnt() for i in range(self.getFacetNumber()))
        return self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax  # 可优化
    # 新加入显示切片


if __name__ == "__main__":  # 展示截交拼接效果
    path = "./STL/monk.stl"
    stlm = StlModel()
    vtkStlReader = stlm.readStlFile(path)
    print("面片数量：", len(stlm.triangles))
    stlm.getBounds()
    slicem = SliceModel(stlm, 1, 'optimal')
    vtkAdaptor = VtkAdaptor()
    vtkAdaptor.drawPdSrc(vtkStlReader).GetProperty().SetOpacity(0.5)
    for i in range(len(slicem.layers)):
        ld = LinkSegs_dlook(slicem.layers[i].segments)  # 拼接
        for j in ld.contours:
            segActor = vtkAdaptor.drawPolyline(j)
            segActor.GetProperty().SetColor(0, 1, 0)
    vtkAdaptor.display()
