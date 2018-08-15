from django.conf.urls import url
from accounts import views, printing
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
app_name = 'accounts'

urlpatterns = [
#    url(r'^user_login/$',  views.user_login,name='user_login'),
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'user/login'}, name='logout'),
    url(r'^register/$',views.register,name='register'),
   # url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.profile, name='profile'),
    url(r'personal/(?P<username>[a-zA-Z0-9]+)$', views.personal_profile, name='personal_profile'),
    url(r'personal/edit/(?P<username>[a-zA-Z0-9]+)$', views.edit_personal_profile, name='edit_personal_profile'),
    url(r"delete/(?P<pk>\d+)/(?P<username>[a-zA-Z0-9]+)/$", views.delete_weight, name='delete_weight'),
    url(r'personal/add/(?P<username>[a-zA-Z0-9]+)$', views.add_weight, name='add_weight'),
    url(r'personal/chart/(?P<username>[a-zA-Z0-9]+)$', views.chart_visualsion, name='chart'),
    url(r'personal/chart/filter/(?P<username>[a-zA-Z0-9]+)$', views.chart, name='filter'),
    url(r"users/$", views.get_users, name="all_users"),
    url(r"users/report/$", views.print_users, name="print_users"),
    url(r"reports/$", views.GeneratePdf_of_all_user, name="all_users_report"),
    url(r"report/(?P<username>[a-zA-Z0-9]+)$", views.GeneratePdf, name="report"),
    url(r'personal/report/filter/$', views.generate_reports, name='filter_report'),

]