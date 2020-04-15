from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  #required signin to view profile 
from django.contrib import messages #display some temporary message
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm



#register page
def register(request):
	if request.method == 'POST': #requested when submit is clicked
		form = UserRegisterForm(request.POST) 
		if form.is_valid(): #check if all data enter is valid
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created ')
			#popup temporary message

			return redirect('users:login')

	else:
		form = UserRegisterForm() # when we render register page
	return render(request, 'entrance/register.html', {'form':form}) 
    

#profile page
@login_required # (decorators) login required if not redirected to login page
def profile(request):
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST, instance = request.user) 
		 #request post data and populate the form with updated user

		p_form = ProfileUpdateForm(request.POST, #request post data
								    request.FILES, #request image file uploaded by users
								    instance = request.user.profile) # populate the form with updated profile

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!!')
			#popup temporary message
			return redirect('profile')


	else:
		current_user = User.objects.get(username=request.user)
		u_form = UserUpdateForm(instance = request.user) #populate the form with current user
		p_form = ProfileUpdateForm(instance = request.user.profile) #populate the form with current profile


	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'entrance/profile.html', context)
