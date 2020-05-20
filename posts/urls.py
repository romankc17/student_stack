from django.urls import path


from . import views,ajax


urlpatterns=[
    path('question/<slug:question_sem>/', views.question_view , name = 'questions'),
    path('question_create/', views.question_create_view, name='question_create'),
    path('question/<slug:slug>/detail/', views.question_answers, name='question_detail'),
    path('answer/', views.AnswerView.as_view(), name='answer'),
    path('question/<slug:slug>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),

    path('load-batches/', ajax.load_batches, name='load_batches'),
    path('load-subjects/', ajax.load_subjects, name='load_subjects'),
]
