from django.conf.urls import (url)

from nutrition import views


urlpatterns = [
    url(r"^$", views.plan_list, name="list"),
    url(r'^create_plan/$', views.create_plan, name='create_plan'),
    url(r'^(?P<plan_id>[0-9]+)/create_nutrition/$', views.create_nutrition, name='create_nutrition'),
    url(r'^(?P<plan_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<plan_id>[0-9]+)/delete_plan/$', views.delete_plan, name='delete_plan'),
    url(r'^(?P<plan_id>[0-9]+)/delete_nutrition/(?P<nutrition_id>[0-9]+)/$', views.delete_nutrition, name='delete_nutrition'),

]
