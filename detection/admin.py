from django.contrib import admin

# Register your models here.
from .models import Camera

class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'detection_choice', 'cam_sys_name', 'registered', 'updated']
    search_fields = ['name', 'detection_choice']

admin.site.register(Camera, CameraAdmin)