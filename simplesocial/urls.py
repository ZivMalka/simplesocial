
from django.urls import path, include
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r"notification/", views.get_latest_notifications, name='latest'),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r'^user/', include('accounts.urls')),
    url(r"^posts/", include('posts.urls', namespace='posts')),
    url(r"^groups/", include('groups.urls', namespace='groups')),
    url(r"^activities/", include('activities.urls', namespace='activities')),
    url(r"^nutrition/", include('nutrition.urls', namespace='nutrition')),
    url(r"^workout/", include('workout.urls', namespace='workout')),
    url(r"messenger/", include('messenger.urls', namespace='messenger')),
    url(r"^appointments/", include('appointments.urls', namespace='appointments')),
    url(r'^notifications/', include('notify.urls', 'notifications')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
