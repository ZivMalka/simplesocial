from django.conf.urls import url

from . import views

app_name='posts'


from .views import (
    PostLikeAPIToggle,
)

urlpatterns = [
    url(r"^$", views.PostList.as_view(), name="all"),
    url(r"new/$", views.CreatePost.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$",views.UserPosts.as_view(),name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
 #   url(r"like/(?P<slug>[-\w]+)/$", views.like.as_view(), name="like"),
    url(r"like/(?P<slug>[-\w]+)/$", views.like.as_view(), name="like"),
    url(r'^api/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    url(r"^posts/in/(?P<slug>[-\w]+)/$", views.SingleGroup.as_view(), name="single_2"),

]
