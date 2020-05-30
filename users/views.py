from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  #required signin to view profile 
from django.contrib import messages #display some temporary message
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileForm

#register page
from .models import Profile


def register(request):
	if request.method == 'POST': #requested when submit is clicked
		print('till')
		u_form = UserRegisterForm(request.POST)
		p_form = ProfileForm (request.POST)
		if u_form.is_valid() and p_form.is_valid(): #check if all data enter is valid
			u_form.save()
			user_ = u_form.cleaned_data.get('username')
			city = p_form.cleaned_data['city']
			gender = p_form.cleaned_data['gender']
			college = p_form.cleaned_data['college']
			faculty = p_form.cleaned_data['faculty']
			batch = p_form.cleaned_data['batch']
			['city', 'college', 'faculty', 'batch', 'gender']
			profile = Profile(user=User.objects.get(username=user_),city=city, gender=gender,college=college,faculty=faculty,batch=batch )
			profile.save()
			messages.success(request, "Account Successfully Created!!")
			return redirect('login')
		else:
			print('not valid')
			print(p_form.errors)

	else:
		u_form = UserRegisterForm()
		p_form = ProfileForm()
	context={
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request, 'entrance/register.html', context)
    

#profile page
@login_required # (decorators) login required if not redirected to login page
def profile(request):
	user = request.user
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST, instance = user)
		 #request post data and populate the form with updated user

		p_form = ProfileForm(request.POST, #request post data
								    request.FILES, #request image file uploaded by users
								    instance = user.profile) # populate the form with updated profile

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!!')
			#popup temporary message
			return redirect('profile',username=user)


	else:
		u_form = UserUpdateForm(instance = user) #populate the form with current user
		p_form = ProfileForm(instance = user.profile) #populate the form with current profile


	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'entrance/profile.html', context)



@login_required
def profile_view(request, username):
	print('till')
	context={
		'profile': get_object_or_404 (Profile, user=User.objects.get(username=username))
	}
	return render(request, 'users/profile.html', context)

@login_required
def profile_update_view(request, user_):
	if request.user != user_:
		raise Http404()




