from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from rooms.models import User
from django.contrib.auth import authenticate, login, logout
from rooms.forms import MyUserCreationForm


def login_view(request):
	if request.user.is_authenticated :
		return redirect('rooms:rooms')
	else:
		Page = 'login'
		if request.method == 'POST':
			email = request.POST["email"]
			password = request.POST["password"]

			try:
				user = User.objects.get(email=email)
				# print(user.email)
				# print(user.id)
			except:
				messages.error(request, 'The email does not exists')

			else:
				user = authenticate(request, email=email, password=password)


				if user is not None :
					# print('hello')
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
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			login(request, user)
			return redirect('rooms:rooms')
	form = MyUserCreationForm()
	context = {'form':form}
	return render(request, 'login.html', context )



def logout_view(request):
	logout(request)
	return redirect('rooms:rooms')
