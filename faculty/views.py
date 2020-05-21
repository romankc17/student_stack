from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from .models import Category,Batch,Subject
from posts.models import Question


class CategoriesList(ListView):
    model = Category
    context_object_name = 'categories'

def subjects_view(request, category, batch):
    subjects = Subject.objects.filter(category=Category.objects.get(slug=category), batch=Batch.objects.get(batch=batch))
    context={'subjects':subjects}
    return render(request, 'faculty/subjects.html', context)

def particular_questions(request, slug):
    try:
        try:
            category = Category.objects.get(slug=slug)
            print(category)
            questions = Question.objects.filter(category=category)
            context = {'questions': questions,
                       'category':category}
        except :
            print('till')
            subject = Subject.objects.get(slug=slug)
            print(subject)
            questions = Question.objects.filter(subject=subject)
            context = {'questions': questions,
                       'category':subject.category,
                       'batch':subject.batch,
                       'subject':subject}
    except:
        raise Http404()



    return render(request, 'faculty/part-questions.html', context)