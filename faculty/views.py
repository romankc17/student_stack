from django.shortcuts import render
from django.views.generic import ListView

from .models import Category,Batch,Subject

class CategoriesList(ListView):
    model = Category
    context_object_name = 'categories'

def subjects_view(request, category, batch):
    subjects = Subject.objects.filter(category=Category.objects.get(slug=category), batch=Batch.objects.get(batch=batch))
    context={'subjects':subjects}
    return render(request, 'faculty/subjects.html', context)