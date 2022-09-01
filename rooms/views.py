from django.shortcuts import render, redirect
from .models import Room, Book, Message
from .forms import RoomForm, MessageForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages


def rooms(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	rooms = Room.objects.filter(
		Q(topic__name__icontains=q)|
		Q(topic__context__icontains=q))
	Topics = Book.objects.all()
	room_count = rooms.count()
	context = {'rooms': rooms, 'topics': Topics, 'room_count': room_count }
	return render(request, 'rooms/rooms.html', context )



def room(request, pk):
	room = Room.objects.get(id=pk)
	topic = room.topic
	room_messages = room.message_set.all()
	participants = room.participants.all()

	if request.method == 'POST':
		if request.user.is_authenticated:
			message = Message.objects.create(
				host=request.user,
				room=room,
				body=request.POST.get('body'))
			participants = room.participants.add(request.user)
			return redirect('rooms:room', pk=room.id)
		else: 
			messages.error(request, 'you are not allowed to send message')
			return render(request, 'login.html')

	context = {'room' :room, 'messages':room_messages, 'participants':participants, 'topic':topic}
	return render(request, 'rooms/room.html', context )


@login_required(login_url='login')
def edit_view(request, pk):
	room = Room.objects.get(id=pk)
	form = RoomForm(instance=room)
	if request.user == room.admin :
		if request.method == "POST" :
			form = RoomForm(request.POST, request.FILES, instance=room)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.admin = request.user
				obj.save()
				return redirect('rooms:rooms')
		context = {'form' : form }
		return render(request, 'rooms/roomEdit.html', context )
	else :
		return redirect('rooms:rooms')


@login_required(login_url='login')
def delete_view(request, pk):
	room = Room.objects.get(id=pk)
	context = {'obj' :room}
	if request.user == room.admin :
		if request.method == 'POST':
			room.delete()
			return redirect('rooms:rooms')
		return render(request, 'rooms/roomDelete.html', context )
	else :
		return redirect('rooms:rooms')

# Create your views here.
@login_required(login_url='login')
def create_view(request):
	form = RoomForm()
	if request.method == "POST" :
		form = RoomForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.admin = request.user
			obj.save()
			return redirect('rooms:rooms')
	context = {'form' : form }
	return render(request, 'rooms/roomCreate.html', context )




@login_required(login_url='login')
def message_edit(request, pk):
	message = Message.objects.get(id=pk)
	room = message.room
	form = MessageForm(instance=message)
	if request.user == message.host :
		if request.method == "POST" :
			form = MessageForm(request.POST, instance=message)
			obj = form.save()
			return redirect('rooms:room', pk=room.id)
		context = {'form' : form }
		return render(request, 'rooms/roomEdit.html', context )
	else :
		return redirect('rooms:room', pk=room.id)



@login_required(login_url='/login')
def message_delete(request, pk):
	message = Message.objects.get(id=pk)
	boom = message.room
	context = {'obj' : message }
	if request.user == message.host :
		if request.method == 'POST':
			message.delete()
			return redirect('rooms:room', pk=boom.id)
		return render(request, 'rooms/roomDelete.html', context )
	else :
		return redirect('rooms:room', pk=boom.id)


def book_list(request):
	books = Book.objects.all().order_by('name') 
	return render(request, 'rooms/book_list.html', {'books' : books} )


@login_required(login_url='/login/')
def book_create(request):
	if request.method == 'POST':
		form = forms.BookForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reader = request.user
			instance.save()
			return redirect( 'rooms:rooms')
	else:
		form = forms.BookForm()
	return render(request, 'rooms/book_creation.html', {'form' : form} )

def book_detail(request, slug ):
	book = Book.objects.get(slug=slug) 
	return render(request, 'rooms/book_detail.html', {'book' : book} )