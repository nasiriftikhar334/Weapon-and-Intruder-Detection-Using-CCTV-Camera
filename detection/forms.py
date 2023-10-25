from django import forms

from .models import Camera

class CameraForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    # name = forms.CharField(error_messages={"required": "Name already exists."})
    # cam_sys_name = forms.CharField(error_messages={"required": "Camera already exists."})
    
    class Meta:
        model = Camera
        fields = ['name', 'detection_choice', 'cam_sys_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-crispy-forms
        for field in self.fields:
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['name'].label = 'Name'
        self.fields['detection_choice'].label = 'Detection'
        self.fields['cam_sys_name'].label = 'Camera'
