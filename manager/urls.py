from django.conf.urls import url
from . import views

app_name = 'manager'

urlpatterns = [
    url(r"menu/$", views.manager_control, name="manager"),
    url(r"workout/(?P<username>[-\w]+)/$", views.work_list, name="work_list"),
    url(r"plans(?P<username>[-\w]+)/$", views.plan_list, name="list"),
]


