from django.http.response import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Camera, object_list
from django.http import Http404
from .utils import dev_list
from .forms import CameraForm

# Create your views here.


def gen(camera, cam):
	device_list = dev_list()
	choice = None
	for x in object_list:
		if x.cam_sys_name==device_list[cam]:
			choice = x.choice

	if choice.lower()=="intruder":
		while True:
			frame = camera.face_detection_frame()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	
	if choice.lower()=="weapon":
		while True:
			frame = camera.weapon_detection_frame()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@login_required(login_url='login')
def video_feed(request, cam):
	device_list = dev_list()
	for x in object_list:
		if x.cam_sys_name == device_list[cam]:
			object = x
    

	return StreamingHttpResponse((gen(object,cam)), content_type='multipart/x-mixed-replace; boundary=frame')



@login_required
def camera_list_view(request):
    qs = Camera.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "cameras/list.html", context=context)


@login_required
def camera_add_view(request):
    form = CameraForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        camera_object = form.save()
        context['form'] = CameraForm()
        # return redirect("cameras:detail", name=camera_object.name)
        return redirect(camera_object.get_absolute_url())
        
    return render(request, "cameras/add.html", context=context)

@login_required
def camera_detail_view(request, name=None):
    camera_obj = None
    if name is not None:
        try:
            camera_obj = Camera.objects.get(name=name)
        except Camera.DoesNotExist:
            raise Http404
        except Camera.MultipleObjectsReturned:
            camera_obj = Camera.objects.filter(name=name).first()
        except:
            raise Http404
    context = {
        "object": camera_obj,
    }
    return render(request, "cameras/detail.html", context=context)
