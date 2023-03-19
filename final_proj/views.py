from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera

# Create your views here.
import device

device_list = device.getDeviceList()
index_device_list = []
for x in device_list:
	index_device_list.append(device_list.index(x))



def index(request):
	context = {
		'device_index': index_device_list
	}
	return render(request, 'streamapp/home.html', context=context)


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request, cam):
	return StreamingHttpResponse(gen(VideoCamera(cam)), content_type='multipart/x-mixed-replace; boundary=frame')

