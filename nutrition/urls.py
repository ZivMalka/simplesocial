from django.conf.urls import (url)

from nutrition import views
app_name = 'nutrition'

urlpatterns = [
    url(r"menu/(?P<username>[-\w]+)/$", views.plan_list, name="list"),
    url(r'^create_plan/$', views.create_plan, name='create_plan'),
    url(r'^(?P<plan_id>[0-9]+)/create_nutrition/$', views.create_nutrition, name='create_nutrition'),
    url(r'^(?P<plan_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<plan_id>[0-9]+)/delete_plan/$', views.delete_plan, name='delete_plan'),
    url(r'^(?P<plan_id>[0-9]+)/delete_nutrition/(?P<nutrition_id>[0-9]+)/$', views.delete_nutrition, name='delete_nutrition'),
    url(r'^(?P<plan_id>[0-9]+)/edit_meal/(?P<nutrition_id>[0-9]+)/$', views.edit_meal, name='edit_meal'),
    url(r'^(?P<plan_id>[0-9]+)/edit_plan/$', views.edit_plan, name='edit_plan'),
    url(r"plans(?P<username>[-\w]+)/$", views.plan_list_manage, name="plan_list"),
]

