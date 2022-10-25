from django.contrib import admin
from . import models
from .models import Room, Message, Book, Comment, CommentLike, MessageLike, BookRating, User
# Register your models here.

admin.site.register(models.Room)
admin.site.register(models.Message)
admin.site.register(models.Book)
admin.site.register(models.Comment)
admin.site.register(models.CommentLike)
admin.site.register(models.MessageLike)
admin.site.register(models.BookRating)
admin.site.register(models.User)