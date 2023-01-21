from django.forms import ModelForm
from .models import Room, Book, Message, Comment, BookRating, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'password1', 'password2']
			

class RoomForm(ModelForm):
	class Meta:
		model = Room
		fields = ['topic', 'name']


class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['body']


class BookForm(ModelForm):
	class Meta():
		model = Book
		fields = ['name', 'authors', 'context', 'slug', 'picture', 'pdf']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['avatar', 'name', 'username', 'email', 'bio']


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body']


class BookRatingForm(ModelForm):
	class Meta:
		model = BookRating
		fields = ['rate']