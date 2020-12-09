from django import forms
from django.db.models import Q

from faculty.models import Batch, Subject
from .models import Question,Image, Answer

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        widgets = {'title':forms.Textarea(attrs={'rows': 3, 'cols': 44})}
        fields=['title','category', 'batch','subject']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.none()
        self.fields['subject'].queryset = Subject.objects.none()
        print(self.data)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['batch'].queryset = Batch.objects.filter(category__id=category_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['batch'].queryset = self.instance.category.batches.all()

        if 'batch' in self.data:
            try:
                batch_id = int(self.data.get('batch'))
                self.fields['subject'].queryset = Subject.objects.filter(Q(category=category_id),Q(batch=batch_id))
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.batch.subject_set.all()



class ImageForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Image
        fields=['image']

    image.widget.attrs["value"] = 'Upload'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        widgets = {'title': forms.Textarea(attrs={'rows': 7, })}
        fields = ['title']


