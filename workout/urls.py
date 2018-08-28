from django.conf.urls import (url)

from workout import views
app_name = 'workout'

urlpatterns = [
    url(r"menu/(?P<username>[-\w]+)/$", views.overview, name="overview"),
    url(r"menu/$", views.manageView, name="manageView"),
    url(r'^add_workout/$', views.add_workout, name='add_workout'),
    url(r'^(?P<workout_id>[0-9]+)/add_set/$', views.add_set, name='add_set'),
    url(r'^(?P<workout_id>[0-9]+)/$', views.view, name='view'),
    url(r'^(?P<workout_id>[0-9]+)/delete_workout/$', views.delete_workout, name='delete_workout'),
    url(r'^(?P<workout_id>[0-9]+)/delete_set/(?P<set_id>[0-9]+)/$', views.delete_set, name='delete_set'),
    url(r'^(?P<workout_id>[0-9]+)/edit_set/(?P<set_id>[0-9]+)/$', views.edit_set, name='edit_set'),
    url(r'^(?P<workout_id>[0-9]+)/edit_workout/$', views.edit_workout, name='edit_workout'),


]

