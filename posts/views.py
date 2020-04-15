from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView, DeleteView

from .forms import QuestionCreateForm,ImageForm

from .models import Question, Image


def question_view(request, question_sem):
    try:
        objects = Question.objects.filter(semester=question_sem)
    except:
        raise Http404
    return render(request, 'posts/questions_list.html', {'objects':objects})


@login_required
def question_create_view(request):

    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm,
                                        extra=5)

    if request.method == 'POST':
        qform = QuestionCreateForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())
        if qform.is_valid() and formset.is_valid():
            qform = qform.save(commit=False)
            qform.user = request.user
            qform.save()
            print(formset.cleaned_data)
            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    photo = Image(question = qform, image=image)
                    photo.save()
                except:
                    pass
            messages.success(request,  "Posted!")
            return HttpResponseRedirect("/")
        else:
            print (qform.errors, formset.errors)
    else:
        qform = QuestionCreateForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    context = {'qform': qform, 'formset': formset}
    return render(request, 'posts/question_create.html',context)

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False