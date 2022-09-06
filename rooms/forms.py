from django.forms import ModelForm
from .models import Room, Book, Message
from django.contrib.auth.models import User


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
		fields = ['name', 'authors', 'context', 'slug', 'picture']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']
