from django.shortcuts import render, redirect
from .models import Room, Book, Message, Comment, MessageLike, CommentLike, BookRating, User
from .forms import RoomForm, MessageForm, UserForm, CommentForm, BookRatingForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib import messages
from . import forms


def rooms(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	rooms = Room.objects.filter(
		Q(topic__name__icontains=q)|
		Q(topic__context__icontains=q))
	Topics = Book.objects.all()[:5]
	room_count = rooms.count()
	room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
	context = {'rooms': rooms, 'topics': Topics, 'room_count': room_count, 'room_messages':room_messages}
	return render(request, 'rooms/rooms.html', context )


def room(request, pk):
	room = Room.objects.get(id=pk)
	topic = room.topic
	participants = room.participants.all()
	room_messages = room.message_set.all()
	message_comments = None
	like = {}
	for message in room_messages:
		message_comments = message.comment_set.all()
		for comment in message_comments:
			bike = CommentLike.objects.filter(
			Q(user = request.user) & 
			Q(comment = comment)
			)
			comment.like = bool(bike)
		like = MessageLike.objects.filter(
		Q(user = request.user) & 
		Q(message = message)
		)
		message.like = bool(like) 

	if request.method == 'POST':
		if request.user.is_authenticated:
			message = Message.objects.create(
				host=request.user,
				room=room,
				body=request.POST.get('body'))
			participants = room.participants.add(request.user)
			return redirect('rooms:room', pk=room.id)

		else:
			messages.error(request, 'you are not allowed to send any messages')
			return render(request, 'login.html')
	if like :
		context = {'room' :room, 'room_messages':room_messages, 'message_comments':message_comments, 'like':like, 'participants':participants, 'topic':topic}
	else:
		context = {'room' :room, 'room_messages':room_messages, 'message_comments':message_comments, 'participants':participants, 'topic':topic}
	return render(request, 'rooms/room_old.html', context )

# def room(request, pk):
# 	room = Room.objects.get(id=pk)
# 	topic = room.topic
# 	room_messages = room.message_set.all()
# 	participants = room.participants.all()

# 	if request.method == 'POST':
# 		if request.user.is_authenticated:
# 			message = Message.objects.create(
# 				host=request.user,
# 				room=room,
# 				body=request.POST.get('body'))
# 			participants = room.participants.add(request.user)
# 			return redirect('rooms:room', pk=room.id)
# 		else:
# 			messages.error(request, 'you are not allowed to send message')
# 			return render(request, 'login.html')

# 	context = {'room' :room, 'room_messages':room_messages, 'participants':participants, 'topic':topic}
# 	return render(request, 'rooms/room.html', context )



@login_required(login_url='login')
def edit_view(request, pk):
	room = Room.objects.get(id=pk)
	form = RoomForm(instance=room)
	topics = Book.objects.all()
	if request.user == room.admin :
		if request.method == "POST" :
			topic_name = request.POST.get('topic')
			topic, created = Book.objects.get_or_create(name=topic_name, reader=request.user)
			room.name = request.POST.get('name')
			room.topic = topic
			room.save()
			return redirect('rooms:rooms')

		context = {'form':form, 'topics':topics, 'room':room }
		return render(request, 'rooms/roomCreate.html', context )
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


def userprofile(request,  pk):
	user = User.objects.get(id=pk)
	rooms = user.room_set.all()
	room_messages = user.message_set.all()
	topics = Book.objects.all()
	context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
	return render(request, 'rooms/profile.html', context)


# Create your views here.
@login_required(login_url='login')
def create_view(request):
	form = RoomForm()
	topics = Book.objects.all()
	if request.method == "POST" :
		topic_name = request.POST.get('topic')
		book = Book.objects.filter(name=topic_name)
		if not book:
			# book = book_create(request)
			return redirect('rooms:rbook-create', pk=topic_name)
		# topic, created = Book.objects.get_or_create(name=topic_name, reader=request.user)
		book = Book.objects.get(name=topic_name)
		Room.objects.create(
			admin=request.user,
			topic=book,
			name=request.POST.get('name')
		)
		return redirect('rooms:rooms')
	context = {'form' : form, 'topics':topics }
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

@login_required(login_url='login')
def comment_edit(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	room = message.room
	form = CommentForm(instance=comment)
	if request.user == comment.owner :
		if request.method == "POST" :
			form = CommentForm(request.POST, instance=comment)
			obj = form.save()
			return redirect('rooms:room', pk=room.id)
		context = {'form' : form }
		return render(request, 'rooms/roomEdit.html', context )
	else :
		return redirect('rooms:room', pk=room.id)



@login_required(login_url='/login')
def comment_delete(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	boom = message.room
	context = {'obj' : comment }
	if request.user == comment.owner :
		if request.method == 'POST':
			comment.delete()
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


@login_required(login_url='/login/')
def rbook_create(request, pk):
	if request.method == 'POST':
		form = forms.BookForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.reader = request.user
			instance.save()
			return redirect( 'rooms:create')
	else:
		form = forms.BookForm(initial={'name': pk})
	return render(request, 'rooms/book_creation.html', {'form' : form} )

def book_detail(request, slug ):
	book = Book.objects.get(slug=slug)
	return render(request, 'rooms/book_detail.html', {'book' : book} )

@login_required(login_url='login')
def editUser(request):
	user = request.user
	form = UserForm(instance=user)
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('rooms:user-profile', pk=user.id)

	context = {'form':form}
	return render(request, 'rooms/edit-user.html', context)



def topicsPage(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	topics = Book.objects.filter(name__icontains=q)
	context = { 'topics':topics }
	return render(request, 'rooms/topics.html', context )


def activityPage(request):
	room_messages = Message.objects.all()
	context = {'messages': room_messages}
	return render(request, 'rooms/activity.html', context)


@login_required(login_url='login')
def comment_create_view(request, pk):
	form = CommentForm()
	message = Message.objects.get(id=pk)
	room = message.room
	if request.method == "POST" :
		comment = Comment.objects.create(
			owner=request.user,
			message=message,
			body=request.POST.get('body'))
		participants = room.participants.add(request.user)
		return redirect('rooms:room', pk=room.id)
	context = {'form' : form }
	return render(request, 'rooms/roomCreate_old.html', context )



@login_required(login_url='login')
def message_like(request, pk):
	message = Message.objects.get(id=pk)
	room = message.room
	like = MessageLike.objects.filter(
	Q(user = request.user) & 
    Q(message = message)
    ) 
	if not like:
		message_like = MessageLike.objects.create(
			user = request.user,
			message = message)
		participants = room.participants.add(request.user)
	else:
		MessageLike.objects.filter(
			Q(user = request.user) & 
			Q(message = message)).delete()	
	return redirect('rooms:room', pk=room.id)
	


@login_required(login_url='login')
def comment_like(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	room = comment.message.room
	like = CommentLike.objects.filter(
	Q(user = request.user) & 
    Q(comment = comment)
    ) 
	if not like:
		comment_like = CommentLike.objects.create(
			user = request.user,
			comment = comment)
		participants = room.participants.add(request.user)
	else:
		CommentLike.objects.filter(
			Q(user = request.user) & 
			Q(comment = comment)).delete()		
	return redirect('rooms:room', pk=room.id)


@login_required(login_url='login')
def book_rate(request, pk):
	book = Book.objects.get(id=pk)
	room = Room.objects.filter(topic=book)
	score = BookRating.objects.filter(
		Q(user = request.user) & 
	    Q(book = book)
	    )
	if request.method == "POST" :
		
		if not score:
			rate = request.POST.get('star') 
			book_rate = BookRating.objects.create(
				user = request.user,
				book = book,
				rate = int(rate)
				)
		else:
			score = BookRating.objects.get(
				Q(user = request.user) & 
			    Q(book = book)
			    )
			id = score.id
			score = BookRating.objects.get(id=id)
			rate = request.POST.get('star')
			print(rate) 
			score.rate = int(rate)
			score.save()
			book = score.book
		return redirect('rooms:book', pk=book.id)
	return render(request, 'rooms/star.html' )


def book(request, pk):
	room = Room.objects.get(id=pk)
	book = room.topic
	score = BookRating.objects.filter(book=book)
	count = score.count()
	print(count)
	s = 0
	if count > 0 :
		for i in range(count):
			rate = score[i]
			s = s + rate.rate
		rating = float(s)/float(count)
		book.rate = rating
		book.save()
	context = {'book':book}
	return render(request, 'rooms/book_detail.html', context )

 
def show_pdf(request, pk):
	book = Book.objects.get(id=pk)
	try:
	    response = book.pdf.url
	    return redirect(response)
	except ValueError:
		messages.error(request, 'there is not any pdf files')
		return redirect('rooms:book', pk=book.id)
