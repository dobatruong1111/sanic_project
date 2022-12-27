import vtk

path = "./data"

colors = vtk.vtkNamedColors()

cone = vtk.vtkConeSource()
cone.SetResolution(10)

map = vtk.vtkPolyDataMapper()
map.SetInputConnection(cone.GetOutputPort())

property = vtk.vtkProperty()
property.SetColor(colors.GetColor3d("tomato"))

actor = vtk.vtkActor()
actor.SetMapper(map)
actor.SetProperty(property)

cam = vtk.vtkCamera()
matrix = vtk.vtkMatrix4x4()

render = vtk.vtkRenderer()
render.SetBackground(colors.GetColor3d("White"))

dicomImageReader = vtk.vtkDICOMImageReader()
dicomImageReader.SetDirectoryName(path)
dicomImageReader.Update()

volMap = vtk.vtkSmartVolumeMapper()
volMap.SetBlendModeToComposite()
volMap.SetRequestedRenderModeToGPU()
volMap.SetInputData(dicomImageReader.GetOutput())

volProperty = vtk.vtkVolumeProperty()
volProperty.ShadeOn()
volProperty.SetInterpolationTypeToLinear()
# Lighting
volProperty.SetDiffuse(0.9)
volProperty.SetSpecular(0.2)

gradientOpacity = vtk.vtkPiecewiseFunction()
gradientOpacity.AddPoint(0, 0)
gradientOpacity.AddPoint(2000, 1)

scalarOpacity = vtk.vtkPiecewiseFunction()
scalarOpacity.AddPoint(-800, 0)
scalarOpacity.AddPoint(-750, 1)
scalarOpacity.AddPoint(-350, 1)
scalarOpacity.AddPoint(-300, 0)
scalarOpacity.AddPoint(-200, 0)
scalarOpacity.AddPoint(-100, 1)
scalarOpacity.AddPoint(1000, 0)
scalarOpacity.AddPoint(2750, 0)
scalarOpacity.AddPoint(2976, 1)
scalarOpacity.AddPoint(3000, 0)

color = vtk.vtkColorTransferFunction()
color.AddRGBPoint(-750, 0.08, 0.05, 0.03)
color.AddRGBPoint(-350, 0.39, 0.25, 0.16)
color.AddRGBPoint(-200, 0.8, 0.8, 0.8)
color.AddRGBPoint(2750, 0.7, 0.7, 0.7)
color.AddRGBPoint(3000, 0.35, 0.35, 0.35)

volProperty.SetGradientOpacity(gradientOpacity)
volProperty.SetScalarOpacity(scalarOpacity)
volProperty.SetColor(color)