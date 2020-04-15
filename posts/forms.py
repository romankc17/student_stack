from django import forms

from .models import Question,Image

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        widgets = {'title':forms.Textarea(attrs={'rows': 2, 'cols': 15})}
        fields=['title',]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields=['image']