from django.conf.urls import (url)

from workout import views
app_name = 'workout'

urlpatterns = [
    url(r"menu/(?P<username>[-\w]+)/$", views.overview, name="overview"),
    url(r'^add_workout/(?P<username>[a-zA-Z0-9]+)$', views.add_workout, name='add_workout'),
    url(r'^(?P<workout_id>[0-9]+)/add_set/$', views.add_set, name='add_set'),
    url(r'^(?P<workout_id>[0-9]+)/view/$', views.view, name='view'),

    url(r'^(?P<workout_id>[0-9]+)/delete_workout/(?P<username>[-\w]+)/$', views.delete_workout, name='delete_workout'),
    url(r'^(?P<workout_id>[0-9]+)/delete_set/(?P<set_id>[0-9]+)/$', views.delete_set, name='delete_set'),
    url(r'^(?P<workout_id>[0-9]+)/edit_set/(?P<set_id>[0-9]+)/(?P<username>[-\w]+)/$', views.edit_set, name='edit_set'),
    url(r'^(?P<workout_id>[0-9]+)/edit_workout/(?P<username>[-\w]+)/$', views.edit_workout, name='edit_workout'),
    url(r"workout/(?P<username>[-\w]+)/$", views.work_list_manage, name="work_list_manage"),

]

