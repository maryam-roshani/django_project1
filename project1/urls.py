from django.contrib import admin
from django.urls import path, re_path as url
from django.urls import include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rooms import views as room_views




urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', room_views.rooms),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^rooms/', include('rooms.urls')),
	]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


