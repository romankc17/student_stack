from django.contrib import messages
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView

from .forms import QuestionCreateForm,QuestionImageForm

from .models import Question, Image


def question_view(request, question_sem):
    try:
        objects = Question.objects.filter(question_sem=question_sem)
    except:
        raise Http404
    return render(request, 'posts/questions_list.html', {'objects':objects})

'''def question_create_view(request):
    if request.method == 'POST':
        q_form = QuestionCreateForm(request.POST)
        i_form = QuestionImageForm(request.POST,request.FILES)
        if q_form.is_valid():
            q_form.save()
            q_id = q_form.cleaned_data.get('id')

            if i_form.is_valid():
                image = i_form.cleaned_data.get('image')
                obj = QuestionImageForm(question_image=Question.objects.get(id=q_id),
                                        image = image)
                obj.save()
                messages.success(request, f'Your question has been created!!')
            return redirect('index')
    else:
        q_form = QuestionCreateForm()
        i_form = QuestionImageForm()

    context = {
        'q_form': q_form,
        'i_form': i_form
    }

    return render(request, 'posts/question_create.html', context)'''


def question_create_view(request):
    ImageFormSet = modelformset_factory(Image, form = QuestionImageForm, extra=3)
    if request.method == 'POST':
        q_form = QuestionCreateForm(request.POST)
        i_form = ImageFormSet(request.POST,request.FILES)
        if q_form.is_valid() and i_form.is_valid():
            q_form = q_form.save(commit=False)
            q_form.user = request.user
            q_form.save()

            for form in i_form.cleaned_data:
                image = form['image']
                photo = Image(question = q_form, image = image)
                photo.save()


            messages.success(request, f'Your question has been created!!')
            return redirect('index')
        else:
            print (q_form.errors, i_form.errors)
    else:
            q_form = QuestionCreateForm()
            i_form = ImageFormSet(queryset=Image.objects.none())

    context = {
        'q_form': q_form,
        'i_form': i_form
    }

    return render(request, 'posts/question_create.html',context,)


