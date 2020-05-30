from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
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


def part_cate_or_sub_ques(request, slug):
    try:
        try:
            category = Category.objects.get(slug=slug)
            print(category)
            questions = Question.objects.filter(category=category)
            if category.get_seasons_display != '':
                batch_subjects = Subject.objects.filter(Q(category=category), Q(batch=Batch.objects.get(slug=1)))
                context = {'questions': questions,
                           'category': category,
                           'batch_subjects':batch_subjects}
            else:
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


def part_batch_ques(request, cate_slug, batch_slug):
    category = get_object_or_404(Category, slug=cate_slug)
    batch = get_object_or_404(Batch, slug=batch_slug)
    questions = Question.objects.filter(Q(category=category), Q(batch=batch))
    batch_subjects = Subject.objects.filter(Q(category=category),Q(batch=batch))
    context = {
        'questions':questions,
        'category':category,
        'batch':batch,
        'batch_subjects':batch_subjects
    }

    return render(request, 'faculty/part-questions.html', context)