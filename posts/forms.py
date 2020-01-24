from django import forms

from .models import Question,Image

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        widgets = {'question_title':forms.Textarea(attrs={'rows': 2, 'cols': 15})}
        fields=['question_sem','question_title']

class QuestionImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields=['image']