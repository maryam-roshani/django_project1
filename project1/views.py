from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login_view(request):
	if request.user.is_authenticated :
		return redirect('rooms:rooms')
	else:
		Page = 'login'
		if request.method == 'POST':
			username = request.POST["username"]
			password = request.POST["password"]

			try:
				user = User.objects.get(username=username)
			except:
				messages.error(request, 'The username does not exists')

			else:
				user = authenticate(request, username=username, password=password)

				if user is not None :
					login(request, user)
					if 'next' in request.POST:
						return redirect(request.POST.get('next'))
					else:
						return redirect('rooms:rooms')
				else :
					messages.error(request, 'The password is not correct.')
		context = {'Page':Page}
		return render(request, 'login.html', context )


def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm( request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('rooms:rooms')
	form = UserCreationForm()
	context = {'form':form}
	return render(request, 'login.html', context )



def logout_view(request):
	logout(request)
	return redirect('rooms:rooms')
