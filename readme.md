1.

Test_vtk STL完整可视化流程展示 

涉及py——

VtkAdaptor：为了方便显示封装一个类VtkAdaptor，在应用中，只需创建VtkAdaptor类的对象，并调用display函数即可方便地构建VTK显示场景

2.

slicemodel 截交及其时间展示

涉及py——

slicemodel 将对 StlModel 进行转化，并通过类内的切片函数（sweep/brutal）对模型进行切片。最终将得到的不同高度的切片对象 Layer，保存在 self.layers 中，并进行测试

SliceAlgo liceAlgo 文件主要是实现了扫描平面的功能，通过 intersectStl_sweep，对于输入的 STL 模型，用扫描平面进行截交，并把截交线段存储在对应高度的 Layer 对象中

3.

LinkSegs_dlook 拼接 字典查询法

STL 展示

4.

Test_genCppath 轮廓填充

涉及py——

GenCpPatht 实现对层内轮廓偏置曲线的生成，实现方面主要是通过控制偏置距离小于填充带宽的情况下，不断调用 ClipperAdaptor 文件中的同名函数 offset，获取一系列偏 置曲线。 然后通过 linkToParent 函数，得到子轮廓起始点距离父轮廓的最近点，将两点距离作为 轮廓间最近距离，同时也意味着两点连线是轮廓的最近连接线

PolyPcrSeeker 封装一个用于确定多边形父子关系的类

（clipperaptor）

5.

Test_genDpath方向平行填充

GenDpPath.py主要是通过上述文件完成平行填充路径生成。先通 过 rotatePolygons 函数实现轮廓按输入角度旋转，然后通过 SplitRegion 函数对轮廓进行填充 区域分割，得到若干个单连通区域的轮廓。通过 genScanYs 函数得到对应轮廓范围的 y 轴扫 描线组，用 genHatches 函数截交后用 linkLocalHatches 函数连接成 Z 字形路径，并用 rotatePolygons 反旋转回原角度。

GenHatch.py 实现对于输入轮廓和平行扫描线列表，得到其截交线段，并将截 交线段 Z 字形连接，输出为对应的方向填充

SplitRegion.py 对填充区域进行分区，以保证在整体上能够使用 Z 形对填 充线进行连接。

6.

FindSptRegion.py 支撑区域

Gensptpath 支撑带填充

7.

main整体展示

8.

方向优化

test_finddir展示

FindOptFeedDir原理
