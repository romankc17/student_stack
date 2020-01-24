from django.urls import path


from . import views


app_name='posts'

urlpatterns=[
    path('question/<slug:question_sem>', views.question_view , name = 'questions'),
    path('question_create', views.question_create_view, name='question_create')
]
