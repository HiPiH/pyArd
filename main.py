#!/usr/bin/python3
from myserial import MySerial
#python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000



from picamera import PiCamera
from time import sleep
from io import BytesIO
from PIL import Image
from multiprocessing import Process, Queue



# camera = PiCamera()
# camera.resolution = (2592, 1944)
# camera.framerate = 15


# camera.start_preview()
# sleep(2)

# camera.stop_preview()


from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
import cv2
from base_camera import BaseCamera

app = FastAPI()
templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024*1024


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


# def streamer():
#     while True:
#         stream = BytesIO()
#         camera.capture(stream, 'jpeg')
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                 stream.getvalue() + b'\r\n')


class Camera(BaseCamera):
    def __init__(self):
        super().__init__()

    # over-wride of BaseCamera class frames method
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(Camera()),
                    media_type='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)