from sanic import response
from sanic import Sanic
import numpy as np
import vtk
import config
from sanic.log import logger
import time

app = Sanic('myapp')

@app.on_response
async def res(request, response):
    logger.info("HTTP response")

@app.on_request
async def req(request):
    logger.info("HTTP request")

@app.route("/")
async def home(request):
    '''
    res = open("./templates/index.html").read()
    return response.html(res)
    '''
    logger.info("Here is your log")
    return response.text(str(request.id))

@app.route("/get_image_dicom")
async def handlerGetImageDicom(request):
    image_bytes = getDicomImageBytes(request.query_args) # the raw data bytes in the array
    return response.raw(image_bytes, headers={"content-type":"image/png"})

@app.route("/get_image")
async def handlerGetImage(request):
    image_bytes = getImageBytes(request.query_args)
    # if image_bytes is a byte array ([223, 225, ...])
    # raw_image = Image.open(io.BytesIO(image_bytes))
    # color_matrix = np.array(raw_image.convert("RGB")) # image matrix

    # color_img = cv2.cvtColor(color_matrix, cv2.COLOR_BGR2RGB) # image matrix

    # is_success, im_buf_arr = cv2.imencode(".png", color_img) # encode
    # byte_im = image_bytes.tobytes() # the raw data bytes in the array (png)

    return response.raw(image_bytes, headers={"content-type":"image/png"})

# view matrix (camera)    
def getViewMatrix(args):
    posi = np.zeros((4, 4))
    viewMatrix = np.eye(4)
    for v in args[::-1]:
        angle = float(v[1])
        if v[0] == "elevation": # Rx
            ele = np.array([
                [1, 0, 0, 0],
                [0, np.cos(angle * np.pi / 180), np.sin(angle * np.pi / 180), 0],
                [0, -np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ ele
        if v[0] == "azimuth": # Ry
            azi = np.array([
                [np.cos(angle * np.pi / 180), 0, -np.sin(angle * np.pi / 180), 0],
                [0, 1, 0, 0],
                [np.sin(angle * np.pi / 180), 0, np.cos(angle * np.pi / 180), 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ azi
        if v[0] == "roll": # Rz
            roll = np.array([
                [np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0, 0],
                [np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ roll
        if v[0] == "position":
            position = angle
            posi[2,3] = -position
    return viewMatrix + posi

def getImageBytes(args):
    renWin = vtk.vtkRenderWindow()
    windowToImgFilter = vtk.vtkWindowToImageFilter()
    writer = vtk.vtkPNGWriter()

    viewMatrix = getViewMatrix(args)
    for i in range(4):
        for j in range(4):
            config.matrix.SetElement(i, j, viewMatrix[i,j])
    config.cam.GetViewTransformObject().SetMatrix(config.matrix)
    
    config.render.AddActor(config.actor)
    config.render.SetActiveCamera(config.cam)

    renWin.AddRenderer(config.render)
    renWin.SetSize(300,300)
    renWin.OffScreenRenderingOn()

    windowToImgFilter.SetInput(renWin)
    
    writer.SetInputConnection(windowToImgFilter.GetOutputPort())
    writer.WriteToMemoryOn()
    writer.Write()
    '''
    result = writer.GetResult()
    n = result.GetNumberOfTuples()
    image_bytes = np.zeros(n, np.uint8)
    for i in range(n):
        image_bytes[i] = result.GetTuple1(i)
    '''
    config.render.RemoveActor(config.actor)

    return bytes(memoryview(writer.GetResult()))

# view matrix (volume)
def getDicomViewMatrix(args):
    viewMatrix = np.eye(4)
    for v in args[::-1]:
        angle = float(v[1])
        if v[0] == "elevation": # Rx
            ele = np.array([
                [1, 0, 0, 0],
                [0, np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0],
                [0, np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ ele
        if v[0] == "azimuth": # Ry
            azi = np.array([
                [np.cos(angle * np.pi / 180), 0, np.sin(angle * np.pi / 180), 0],
                [0, 1, 0, 0],
                [-np.sin(angle * np.pi / 180), 0, np.cos(angle * np.pi / 180), 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ azi
        if v[0] == "roll": # Rz
            roll = np.array([
                [np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0, 0],
                [np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            viewMatrix = viewMatrix @ roll
    return viewMatrix

def getDicomImageBytes(args):
    vol = vtk.vtkVolume()
    cam = vtk.vtkCamera()
    dicomRender = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    winToImg = vtk.vtkWindowToImageFilter()
    writer = vtk.vtkPNGWriter()

    vol.SetMapper(config.volMap)
    vol.SetProperty(config.volProperty)
    center = vol.GetCenter()
    vol.SetPosition(-center[0], -center[1], -center[2])

    cam.SetClippingRange(0.1, 5000)
    cam.SetPosition(0, 0, 0.1)

    if len(args) != 0:
        for v in args:
            if v[0] == "roll": cam.Roll(float(v[1]))
            elif v[0] == "azimuth": cam.Azimuth(float(v[1]))
            elif v[0] == "elevation": cam.Elevation(float(v[1]))
            elif v[0] == "position": cam.SetPosition(0, 0, float(v[1]))
    
    dicomRender.SetBackground(config.colors.GetColor3d("White"))
    dicomRender.SetActiveCamera(cam)
    dicomRender.AddVolume(vol)
    
    renWin.AddRenderer(dicomRender)
    renWin.SetSize(300, 300)
    renWin.OffScreenRenderingOn()
    
    winToImg.SetInput(renWin)

    writer.SetInputConnection(winToImg.GetOutputPort())
    writer.WriteToMemoryOn()
    start = time.time()
    writer.Write()
    stop = time.time()
    # print((stop-start)*1000)

    return bytes(memoryview(writer.GetResult()))

if __name__ == "__main__":
    app.run(debug=True, access_log=True)