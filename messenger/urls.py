from django.urls import path, re_path
from messenger import views
from django.conf.urls import url
from .views import ThreadView, InboxView, ConversationListView

app_name = 'messenger'
urlpatterns = [
    path("", InboxView.as_view(), name="messages_list"),
    re_path(r"^(?P<username>[\w.@+-]+)/$", ThreadView.as_view()),
    url(r'^(?P<username>[\w.@+-]+)/$', views.ConversationListView.as_view(),name='conversation_detail'),


]
