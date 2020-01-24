from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import QuestionCreateForm,QuestionImageForm

from .models import Question

def question_view(request, question_sem):
    try:
        objects = Question.objects.filter(question_sem=question_sem)
    except:
        raise Http404
    return render(request, 'posts/questions_list.html', {'objects':objects})

def question_create_view(request):
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

    return render(request, 'posts/question_create.html', context)

