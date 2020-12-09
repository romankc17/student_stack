import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from faculty.models import Batch, Category, Subject


def load_batches(request):
    category_id = request.GET.get('category')
    batches = Batch.objects.filter(category__id=category_id)
    batch_list=[]
    for batch in batches:
        batch_list.append(batch.batch)
    data = {
        'batches':batches,

    }
    # return HttpResponse(data, content_type='application/json')
    return render(request, 'faculty/batch_dropdown_list_options.html', data)
    # return JsonResponse(data)

def load_subjects(request):
    category_id = request.GET.get('category')
    batch_id = request.GET.get('batch')
    print(batch_id)
    subjects = Subject.objects.filter(Q(category=category_id),Q(batch=batch_id))
    data = {
        'subjects':subjects,
    }
    # return HttpResponse(data, content_type='application/json')
    return render(request, 'faculty/subject_dropdown_list_options.html', data)
    # return JsonResponse(data)