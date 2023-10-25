from django.shortcuts import render
from detection.models import Camera
from detection.utils import dev_list
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
	registered_cam = Camera.objects.all()
	device_list = dev_list()
	index_device_list = []
	for x in registered_cam:
		for y in device_list:
			if x.cam_sys_name==y:
				index_device_list.append(device_list.index(y))
	context = {
		'device_index': index_device_list
	}
	return render(request, 'streamapp/home.html', context=context)
