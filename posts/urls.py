from django.conf.urls import url

from . import views

app_name='posts'


urlpatterns = [

    url(r"^$", views.PostList.as_view(), name="all"),
   # url(r"new/$", views.writePost, name="create"),
    url(r'^post/(?P<pk>\d+)/new/$', views.write_post, name='create'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='comment'),
    url(r"by/(?P<username>[-\w]+)/$",views.UserPosts.as_view(),name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
    url(r"like/(?P<pk>\d+)/$",views.like.as_view() ,name="like"),
 #   url(r"like/(?P<slug>[-\w]+)/$", views.like.as_view(), name="like"),
 #   url(r"like/(?P<slug>[-\w]+)/$", views.like.as_view(), name="like"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$", views.SingleGroup.as_view(), name="single_2"),


]
