from GenSptPath import *
from GenCpPath import *
from IDEndLayers import *
class PrintParams:
    def _init__(self, stlModel):
        self.stlModel = stlModel
        self.layerThk, self.shellThk, self.endThk= 0.2,2.0,2.0
        self.sfRate, self.fillAngle = 0.2,0.0
        self.sptOn = False
        self.sptCrAngle = degToRad(60.0)
        self.sptGridSize = 2.0
        self.sptSfRate, self.sptFillAngle = 0.15,0.0
        self.sptFillType = SptFillType.cross
        self.sptXyGap = 1.0
        self.g0Speed, self.g1Speed = 5000,1000
        self.startCode = "; Start code... .n"
        self.endCode= "; End code...n"
        self.nozzleSize, self.filamentSize = 0.5,1.75

def genAllPaths(pp):  # : PrintParams刪去
    sfInvl = pp.nozzleSize / pp.sfRate
    sptSfInvl = pp.nozzleSize / pp.sptSfRate
    # layers = slice_topo(pp.stlModel, pp.layerThk)
    slicem = SliceModel(pp.stlModel, pp.layerThk, 'optimal')
    layers = slicem.layers  # 读取相应切片文件

    # IdEndLayers(layers, pp.shellThk, int(pp.endThk / pp.layerThk)+ 1)
    for i, layer in enumerate(layers):
        layer.cpPaths, layer.ffPaths, layer.sfPaths =[],[],[]
        layer.cpPaths = genCpPath(layer.contours, pp.nozzleSize, pp.shellThk)
        delta= 0 if i % 2== 0 else math.pi / 2
        if len(layer.ffContours) > 0:
            layer.ffPaths = genDpPath(layer.ffContours,pp.nozzleSize, pp.fillAngle + delta)
        if len(layer.sfContours) > 0:
            layer.sfPaths = genDpPath(layer.sfContours, sfInvl, pp.fillAngle + delta)
    if pp.sptOn:
        genSptPath(pp.stlModel, layers, sptSfInvl, pp.sptGridSize, pp.sptCrAngle,pp.sptFillType, pp.sptFillAngle, pp.sptXyGap)
    return layers

def pathToCode(path, pp, e, nf2):
    code = ""
    for i, p in enumerate(path.points):
        if i == 0:
            code += "G0 F%d X%.3f Y%.3f Z%.3f\n" %(pp.g0Speed, p.x, p.y, p.z)
        else:
            e +=p.distance(path.points[i-1])*nf2
            code += "G1 F%d X%.3f Y%.3f E%.3f\n" %(pp.g1Speed, p.x, p.y, e)
    return code

def postProcess(layers, pp):
    code, e = pp.startCode, 0
    nf2 =(pp.nozzleSize / pp.filamentSize)**2
    for i, layer in enumerate(layers):
        code += "; Layer %d\n" % i
        for path in layer.sptCpPaths: code += pathToCode(path, pp, e, nf2)
        for path in layer.sptDpPaths: code += pathToCode(path, pp, e, nf2)
        for path in layer.cpPaths: code += pathToCode(path, pp, e, nf2)
        for path in layer.ffPaths: code += pathToCode(path, pp, e, nf2)
        for path in layer.sfPaths: code += pathToCode(path, pp, e, nf2)
    print(code+pp.endCode)
    return code + pp.endCode
def genNcCode(pp): # : PrintParams刪去
    layers = genAllPaths(pp)
    return postProcess(layers, pp)



if __name__ == '__main__':
    stlModel = StlModel()
    ath = "./STL/monk.stl"
    src = stlModel.readStlFile(path)
    pp1 = PrintParams(stlModel)
    nc_code = genNcCode(pp1)
    with open('nc.txt','w') as f:
        f.write(nc_code)