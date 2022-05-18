import vtk

# STL模型读取显示

renderer = vtk.vtkRenderer()

renderer.SetBackground(0, 0.5, 0.5)
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(900, 600)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
interactor.Initialize()

stlReader = vtk.vtkSTLReader()
stlReader.SetFileName("./STL/monk.STL")
outlineFilter = vtk.vtkOutlineFilter()
outlineFilter.SetInputConnection(stlReader.GetOutputPort())
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(outlineFilter.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.1, 0.1, 0.1)
renderer.AddActor(actor)

stlMapper = vtk.vtkPolyDataMapper()  # 创建模型显示mapper-actor
stlMapper.SetInputConnection(stlReader.GetOutputPort())
stlActor = vtk.vtkActor()
stlActor.SetMapper(stlMapper)
renderer.AddActor(stlActor)

interactor.Start()
