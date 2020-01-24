from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from . import forms, models


def register(request):
    if request.method == "POST":
        u_form = forms.UserCreateForm(request.POST)
        p_form = forms.ProfileCreateForm(request.POST,  # request post data
                                         request.FILES,  # request image file uploaded by users
                                         )

        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')


            if p_form.is_valid():
                college_name = p_form.cleaned_data.get('college_name')
                semester = p_form.cleaned_data.get('semester')
                profile_image = p_form.cleaned_data.get('profile_image')
                p = models.Profile(user=User.objects.get(username=username),
                                   college_name=college_name,
                                   semester=semester,
                                   profile_image=profile_image)
                p.save()

                messages.success(request, f'Your account has been created!!')
            # popup temporary message

            return redirect('users:login')

    else:
        u_form = forms.UserCreateForm()  # populate the form with current user
        p_form = forms.ProfileCreateForm()  # populate the form with current profile

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)

class ProfileDetailView(generic.DetailView):
    model = models.Profile
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'
    template_name = 'users/profile.html'

