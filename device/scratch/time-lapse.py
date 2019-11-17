#capture picutres forever (no limit) 

from time import sleep
import picamera

with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	for filename in camera.capture_continuous('/home/pi/everysecond/upload/{timestamp:%H-%M-%S-%f}.jpg'):
		sleep(5)
