from django.forms import ModelForm
from .models import Room, Book, Message


class RoomForm(ModelForm):
	class Meta:
		model = Room
		fields = ['topic']
	

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['body']


class BookForm(ModelForm):
	class Meta():
		model = Book
		fields = ['name', 'authors', 'context', 'slug', 'picture']