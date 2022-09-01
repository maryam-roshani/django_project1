from . import views
from django.urls import path, re_path as url
from django.urls import include, re_path


app_name = 'rooms'

urlpatterns = [
	url(r'^$', views.rooms, name='rooms'),
	url(r'^create/', views.create_view, name='create'),
	url(r'^book-create/', views.book_create, name='book-create'),
    path('<str:pk>', views.room, name='room'),
    path('edit/<str:pk>', views.edit_view, name='edit'),
    path('delete/<str:pk>', views.delete_view, name='delete'),
    path('message-edit/<str:pk>', views.message_edit, name='message-edit'),
    path('message-delete/<str:pk>', views.message_delete, name='message-delete'),
]
