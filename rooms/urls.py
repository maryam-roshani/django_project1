from . import views
from django.urls import path, re_path as url
from django.urls import include, re_path


app_name = 'rooms'

urlpatterns = [
	url(r'^$', views.rooms, name='rooms'),
	url(r'^create/', views.create_view, name='create'),
	url(r'^book-create/', views.book_create, name='book-create'),
    path('rbook-create/<str:pk>/', views.rbook_create, name='rbook-create'),
    path('book/<str:pk>/', views.book, name='book'),
    path('show-pdf/<str:pk>/', views.show_pdf, name='show-pdf'),
    path('book-rate/<str:pk>/', views.book_rate, name='book-rate'),
    path('<str:pk>', views.room, name='room'),
    path('profile/<str:pk>', views.userprofile, name='user-profile'),
    path('edit/<str:pk>', views.edit_view, name='edit'),
    path('delete/<str:pk>', views.delete_view, name='delete'),
    path('message-edit/<str:pk>', views.message_edit, name='message-edit'),
    path('message-delete/<str:pk>', views.message_delete, name='message-delete'),
    path('message-like/<str:pk>', views.message_like, name='message-like'),
	url(r'^edit-user/$', views.editUser, name='edit-user'),
	url(r'^topics/$', views.topicsPage, name='topics'),
	url(r'^activity/', views.activityPage, name='activity'),
	path('comment-create/<str:pk>', views.comment_create_view, name='create-comment'),
	path('comment-edit/<str:pk>', views.comment_edit, name='comment-edit'),
    path('comment-delete/<str:pk>', views.comment_delete, name='comment-delete'),
    path('comment-like/<str:pk>', views.comment_like, name='comment-like'),

]
