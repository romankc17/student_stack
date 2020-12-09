from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm #builtin form
from django.forms import ClearableFileInput

from .models import Profile

class UserRegisterForm(UserCreationForm):
	#email = forms.EmailField()
	#first_name= forms.CharField()
	#last_name = forms.CharField()


	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'currently'
    input_text = 'change'
    clear_checkbox_label = ''

class ProfileForm(forms.ModelForm):
	# image = forms.ImageField(widget=MyClearableFileInput)
	class Meta:
		model = Profile
		fields = ['city','college','faculty','batch','gender',]


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

