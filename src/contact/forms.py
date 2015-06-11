from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Contact

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = ('name', 'email', 'message',)