from django.conf.urls import url
from accounts import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
app_name = 'accounts'

urlpatterns = [
#    url(r'^user_login/$',  views.user_login,name='user_login'),
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$',views.register,name='register'),
   # url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.profile, name='profile'),
]