from django.conf.urls import (url)
from appointments import views
app_name = 'appointments'

urlpatterns = [
    url(r"menu/(?P<username>[-\w]+)/$", views.appoint, name='appoint'),
    url(r'^create_event$', views.create_event, name='create_event'),
    url(r'^(?P<appoint_id>[0-9]+)/delete_event/(?P<username>[-\w]+)/$', views.delete_event, name='delete_event'),
    url(r'^(?P<appointment_id>[0-9]+)/edit_event/(?P<username>[-\w]+)/$', views.edit_event, name='edit_event'),
    url(r"manage/appointments/$", views.appointment_manage, name="appointment_manage"),




]

