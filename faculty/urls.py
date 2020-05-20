from django.urls import path


from . import views



urlpatterns=[
    path('', views.CategoriesList.as_view(), name = 'categories'),
    path('s/<slug:category>/<slug:batch>', views.subjects_view, name='subjects')
]