from django import forms
from django.core import validators

class ImageForm(forms.Form):
	image = forms.ImageField(label='Image', required=True)