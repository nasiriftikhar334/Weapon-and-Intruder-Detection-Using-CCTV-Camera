from django.db import models
from .utils import dev_list
from django.urls import reverse
from django.db.models.signals import post_save
from .camera import VideoCamera


device_list = dev_list()
device_list = list(zip(device_list, device_list))

class detectiontype(models.TextChoices):
    NONE = 'None'
    WEAPON = 'Weapon'
    INTRUDER = 'Intruder'

class Camera(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={"unique": "Name already exists."})
    detection_choice = models.CharField(max_length=10, choices=detectiontype.choices, default=detectiontype.NONE)
    cam_sys_name = models.CharField(max_length=50, unique=True, choices=device_list, default=device_list[0], error_messages={"unique": "Camera already exists."})
    registered = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # return f'/cameras/{self.name}/'
        return reverse("camera-detail", kwargs={"name": self.name})

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        # obj.save()
        # do another something


def camera_post_save(sender, instance, created, *args, **kwargs):
    if created:
        add_new_cam_obj(instance)
        
post_save.connect(camera_post_save, sender=Camera)

# List of all objects of videocamera class

object_list = []

def create_cam_objects():
	registered_cam = Camera.objects.all()
	device_list = dev_list()
	# thread_list = []
	for x in registered_cam:
		for y in device_list:
			if x.cam_sys_name==y:
				obj = VideoCamera(device_list.index(y), x)
				object_list.append(obj)

create_cam_objects()

# create and add new camera object of videocamera class

def add_new_cam_obj(instance):
	device_list = dev_list()
	for y in device_list:
		if instance.cam_sys_name==y:
			obj = VideoCamera(device_list.index(y), instance)
			object_list.append(obj)
			print(object_list)