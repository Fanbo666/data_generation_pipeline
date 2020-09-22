#!/usr/bin/python
# -*- coding: UTF-8 -*-
import vtk
 
def main():

 
    # Read from file
    stlreader = vtk.vtkSTLReader()
    stlreader.SetFileName(r"D:\DT-cat_Synthetic_Data_Generation\vtk_generation\mino_3d_model\demo_part\F58001104949503200002.stl")

    tmapper = vtk.vtkTextureMapToCylinder()
    tmapper.SetInputConnection(stlreader.GetOutputPort())
    tmapper.PreventSeamOn()

    xform = vtk.vtkTransformTextureCoords()
    xform.SetInputConnection(tmapper.GetOutputPort())
    xform.SetScale(0.5, 0.5, 0.5)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(xform.GetOutputPort())

    # A texture is loaded using an image reader. Textures are simply images.
    # The texture is eventually associated with an actor.
    #bmpReader = vtk.vtkBMPReader()
    #bmpReader.SetFileName("D:\DT-cat_Synthetic_Data_Generation\\texture\\2.bmp")
    #atext = vtk.vtkTexture()
    #atext.SetInputConnection(bmpReader.GetOutputPort())
    #atext.InterpolateOn()

    cylinderActor = vtk.vtkActor()
    cylinderActor.RotateWXYZ(0,1,0,0)
    cylinderActor.GetProperty().SetColor(0.2,0.3,0.7)
    cylinderActor.SetMapper(mapper) # 设置生成几何图元的Mapper。即连接一个Actor到可视化管线的末端(可视化管线的末端就是Mapper)。
    #cylinderActor.SetTexture(atext)
    
    renderer = vtk.vtkRenderer() # 负责管理场景的渲染过程
    renderer.AddActor(cylinderActor)
    light = vtk.vtkLight()
    light.SetPosition(400,0,00)
    renderer.AddLight(light)
    renderer.SetBackground(0.1, 0.2, 0.4)
    renWin = vtk.vtkRenderWindow() # 将操作系统与VTK渲染引擎连接到一起。
    renWin.AddRenderer(renderer)
    renWin.SetSize(300, 300)
    iren = vtk.vtkRenderWindowInteractor() # 提供平台独立的响应鼠标、键盘和时钟事件的交互机制
    iren.SetRenderWindow(renWin)
 
    # 交互器样式的一种，该样式下，用户是通过控制相机对物体作旋转、放大、缩小等操作
    style = vtk.vtkInteractorStyleTrackballCamera()
    axes=vtk.vtkAxesActor()
    renderer.AddActor(axes)
 
    iren.SetInteractorStyle(style)
    iren.Initialize()
 
    iren.Start()
 
    # Clean up
    # del cylinder
    del stlreader
    del cylinderActor
    del renderer
    del renWin
    del iren
 
main()
