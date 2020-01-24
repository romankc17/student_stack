from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['college_name','semester', 'profile_image']

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester'].label = "Semester"'''