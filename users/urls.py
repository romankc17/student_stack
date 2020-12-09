from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='entrance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='entrance/logout.html'), name='logout'),
    path('update/', views.profile, name='profile_update'),
    path('profile/<slug:username>/', views.profile_view, name='profile')

]


