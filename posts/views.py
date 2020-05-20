from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, DeleteView, DetailView, CreateView
from django.urls import reverse

from faculty.models import Category
from .forms import QuestionCreateForm,ImageForm

from .models import Question, Image
from posts.models import Answer
from posts.forms import AnswerForm


def question_view(request, question_sem):
    try:
        objects = Question.objects.filter(semester=question_sem)
    except:
        raise Http404
    return render(request, 'posts/questions_list.html', {'objects':objects})

def home_page(request):
    context={
        'questions':Question.objects.all().order_by('-created'),
        'categories':Category.objects.all()
    }
    return render(request, 'index.html', context)


def question_create_view(request):
    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm,
                                        extra=1)
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
                print(form)
                try:
                    image = form['image']

                    photo = Image(question = qform, image=image)
                    photo.save()
                except:
                    pass
            messages.success(request,  "Posted!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request,"Sorry Something Went Wrong!")
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

def question_answers(request, slug): # todo answer form with multiple image

    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm,
                                        extra=3)
    question = Question.objects.get(slug = slug)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        formset = ImageFormSet(request.POST,
                               request.FILES,
                               queryset = Image.objects.none())
        if answer_form.is_valid() and formset.is_valid():
            answer_form = answer_form.save(commit=False)
            answer_form.user = request.user
            answer_form.question = question
            answer_form.save()

            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    photo = Image(answer=answer_form, image=image)
                    photo.save()
                except :
                    pass


            messages.success(request, "Answer Posted!")

            return HttpResponseRedirect(reverse('question_detail', kwargs={'slug':question.slug}))


    answer_form = AnswerForm()
    formset = ImageFormSet(queryset=Image.objects.none())

    context = {
        'question':question,
        'answer_form': answer_form,
        'formset': formset,
    }

    return render(request, 'posts/question_detail.html', context)

class AnswerView(CreateView):
    model = Answer
    fields = ['title']
    

