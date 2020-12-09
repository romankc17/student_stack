from django.urls import path


from . import views



urlpatterns=[
    path('', views.CategoriesList.as_view(), name = 'categories'),
    path('s/<slug:category>/<slug:batch>/', views.subjects_view, name='subjects'),
    path('p/questions/<slug:slug>/', views.part_cate_or_sub_ques, name='part_questions'),
    path('p/questions/<slug:cate_slug>/<slug:batch_slug>', views.part_batch_ques, name='part_batch_ques'),
]