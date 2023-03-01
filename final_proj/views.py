from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera

# Create your views here.
import device

device_list = device.getDeviceList()
print(device_list)

def index(request):
	return render(request, 'streamapp/home.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

