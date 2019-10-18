# record one picture per second, for 100 pictures
from time import sleep
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    camera.start_preview()
    sleep(1)

    for i, filename in enumerate(camera.capture_continuous('/home/pi/everysecond/upload/{timestamp:%Y%m%d%H%M%S}.jpg')):
        sleep(2)
    camera.stop_preview()

