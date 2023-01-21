from django.contrib import admin
from . import models
from .models import Song, Playlist, Favourite, Recent
# Register your models here.

admin.site.register(models.Song)
admin.site.register(models.Playlist)
admin.site.register(models.Favourite)
admin.site.register(models.Recent)
