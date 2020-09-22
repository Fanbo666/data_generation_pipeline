import vtk
import os


def set_texture(data_source, mapper, texture_path):
    """
    Set texture for 3d object from a image

    :param data_source: The source of 3d object
    :param mapper: The mapper.
    :param texture_path: The path of the image texture
    :return atext: texture object for actor
    """
    tmapper = vtk.vtkTextureMapToCylinder()
    tmapper.SetInputConnection(data_source.GetOutputPort())
    tmapper.PreventSeamOn()

    xform = vtk.vtkTransformTextureCoords()
    xform.SetInputConnection(tmapper.GetOutputPort())
    xform.SetScale(4, 4, 4)

    mapper.SetInputConnection(xform.GetOutputPort())

    if texture_path:
        path, ext = os.path.splitext(texture_path)
        ext = ext.lower()
    if not ext:
        ext = '.png'
        texture_path = texture_path + ext
    if ext == '.bmp':
        reader = vtk.vtkBMPReader()
    elif ext == '.jpg' or ext == '.jpeg':
        reader = vtk.vtkJPEGReader()
    elif ext == '.pnm':
        reader = vtk.vtkPNMReader()
    elif ext == '.ps':
        if rgba:
            rgba = False
        reader = vtk.vtkPostScriptReader()
    elif ext == '.tiff':
        reader = vtk.vtkTIFFReader()
    else:
        reader = vtk.vtkPNGReader()

    reader.SetFileName(texture_path)
    atext = vtk.vtkTexture()
    atext.SetInputConnection(reader.GetOutputPort())
    atext.InterpolateOn()
    return atext


def set_background_image(image_path):
    """
    Set background to a customized image
    :param image_path: image path
    :return: a background renderer
    """
    if image_path:
        path, ext = os.path.splitext(image_path)
        ext = ext.lower()
    if not ext:
        ext = '.png'
        image_path = image_path + ext
    if ext == '.bmp':
        reader = vtk.vtkBMPReader()
    elif ext == '.jpg':
        reader = vtk.vtkJPEGReader()
    elif ext == '.pnm':
        reader = vtk.vtkPNMReader()
    elif ext == '.ps':
        if rgba:
            rgba = False
        reader = vtk.vtkPostScriptReader()
    elif ext == '.tiff':
        reader = vtk.vtkTIFFReader()
    else:
        reader = vtk.vtkPNGReader()

    reader.SetFileName(image_path)
    reader.Update()
    image_data = reader.GetOutput()
    image_actor = vtk.vtkImageActor()
    image_actor.SetInputData(image_data)

    background_renderer = vtk.vtkRenderer()
    background_renderer.AddActor(image_actor)

    origin = image_data.GetOrigin()
    spacing = image_data.GetSpacing()
    extent = image_data.GetExtent()

    camera = background_renderer.GetActiveCamera()
    camera.ParallelProjectionOn()

    xc = origin[0] + 0.5*(extent[0] + extent[1]) * spacing[0]
    yc = origin[1] + 0.5*(extent[2] + extent[3]) * spacing[1]
    # xd = (extent[1] - extent[0] + 1) * spacing[0]
    yd = (extent[3] - extent[2] + 1) * spacing[1]
    d = camera.GetDistance()
    camera.SetParallelScale(0.5 * yd)
    camera.SetFocalPoint(xc, yc, 0.0)
    camera.SetPosition(xc, yc, d)

    return background_renderer

def WriteImage(fileName, renWin, rgba=True):
    """
    Write the render window view to an image file
    :param fileName: The file name, if no extension then PNG is assumed.
    :param renWin: The render window.
    :param rgba: Used to set the buffer type.
    :return:
    """
    if fileName:
        # Select the writer to use.
        path, ext = os.path.splitext(fileName)
        ext = ext.lower()
        if not ext:
            ext = '.png'
            fileName = fileName + ext
        if ext == '.bmp':
            writer = vtk.vtkBMPWriter()
        elif ext == '.jpg':
            writer = vtk.vtkJPEGWriter()
        elif ext == '.pnm':
            writer = vtk.vtkPNMWriter()
        elif ext == '.ps':
            if rgba:
                rgba = False
            writer = vtk.vtkPostScriptWriter()
        elif ext == '.tiff':
            writer = vtk.vtkTIFFWriter()
        else:
            writer = vtk.vtkPNGWriter()

        windowto_image_filter = vtk.vtkWindowToImageFilter()
        windowto_image_filter.SetInput(renWin)
        windowto_image_filter.SetScale(1)  # image quality
        if rgba:
            windowto_image_filter.SetInputBufferTypeToRGBA()
        else:
            windowto_image_filter.SetInputBufferTypeToRGB()
            # Read from the front buffer.
            windowto_image_filter.ReadFrontBufferOff()
            windowto_image_filter.Update()

        #image = windowto_image_filter.GetOutput()

        # print(image.GetPoint(100,300,0))

        writer.SetFileName(fileName)
        #writer.SetWriteToMemory(1)
        writer.SetInputConnection(windowto_image_filter.GetOutputPort())
        writer.Write()
        #print (len(np.array(writer.GetResult())))
    else:
        raise RuntimeError('Need a filename.')


def uni_rotate(actor, X, Y, Z):
    actor.RotateWXYZ(X, 1, 0, 0)
    actor.RotateWXYZ(Y, 0, 1, 0)
    actor.RotateWXYZ(Z, 0, 0, 1)

