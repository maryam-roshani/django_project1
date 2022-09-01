from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Book(models.Model):
	name = models.CharField(max_length=100)
	authors = models.CharField(max_length=100)
	date_published = models.DateField(auto_now_add=True)
	context = models.TextField()
	slug = models.SlugField(blank=True, null=True)
	picture = models.ImageField(blank=True, upload_to="media")
	reader = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.name

	def snip(self):
		return self.context[:50] + str('...')


# Create your models here.
class Room(models.Model):
	admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	updated = models.DateTimeField(auto_now_add=True)
	created = models.DateTimeField(auto_now=True)
	topic = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	participants = models.ManyToManyField(User, blank=True, related_name='participants')

	def __str__(self):
		return self.topic.name


class Message(models.Model):
	body = models.TextField()
	host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	updated = models.DateTimeField(auto_now_add=True)
	created = models.DateTimeField(auto_now=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.body