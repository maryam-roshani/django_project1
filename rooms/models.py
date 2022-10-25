from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')

        user = self.model(
        		email=self.normalize_email(email),
        		username=username
        	)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
        		email=self.normalize_email(email),
        		username=username,
        		password=password,
        	)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser):
	email = models.EmailField(verbose_name='Email Address', unique=True, null=True)
	username = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=100, null=True)
	bio = models.TextField(null=True)
	avatar = models.FileField(null=True, default="avatar.svg", validators=[FileExtensionValidator(['png', 'svg', 'jpg'])])
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', ]

	objects = CustomUserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Book(models.Model):
	name = models.CharField(unique=True, max_length=100)
	authors = models.CharField(max_length=100, null=True, blank=True)
	date_published = models.DateField(auto_now_add=True)
	context = models.TextField(null=True, blank=True)
	slug = models.SlugField(blank=True, null=True)
	picture = models.FileField(null=True, default="book.jpg", validators=[FileExtensionValidator(['png', 'svg', 'jpg'])])
	pdf = models.FileField(blank=True, upload_to="media")
	reader = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.FloatField(default=0, null=True, blank=True)

	def __str__(self):
		return self.name

	def snip(self):
		return self.context[:50] + str('...')

	def __unicode__(self):
		return self.name


# Create your models here.
class Room(models.Model):
	name = models.CharField(unique=True, max_length=100, null=True)
	admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	updated = models.DateTimeField(auto_now_add=True)
	created = models.DateTimeField(auto_now=True)
	topic = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	participants = models.ManyToManyField(User, blank=True, related_name='participants')

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name


class Message(models.Model):
	body = models.TextField()
	host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	updated = models.DateTimeField(auto_now_add=True)
	created = models.DateTimeField(auto_now=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
	like = models.BooleanField(default=False)

	class Meta:
		ordering = ['-updated', '-created']

		
	def __str__(self):
		return self.body



class Comment(models.Model):
	body = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	updated = models.DateTimeField(auto_now_add=True)
	created = models.DateTimeField(auto_now=True)
	message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
	like = models.BooleanField(default=False)

	class Meta:
		ordering = ['-updated', '-created']

		
	def __str__(self):
		return self.body





class CommentLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class MessageLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	message = models.ForeignKey(Message, on_delete=models.CASCADE)



class BookRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.FloatField(default=0, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

