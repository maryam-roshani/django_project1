from django.db import models
from django.contrib.auth.models import User
from rooms.models import User
import datetime
from django.utils.translation import gettext as _


# Create your models here.

def year_choices():
    return [(r,r) for r in range(1964, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year


class Song(models.Model):

    Language_Choice = (
              ('Persian', 'Persian'),
              ('English', 'English'),
          )



    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    language = models.CharField(max_length=20,choices=Language_Choice,default='Persian')
    song_img = models.FileField(null=True, blank=True)
    year = models.IntegerField(_('year'), choices=year_choices(), default=current_year)
    singer = models.CharField(max_length=200)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

