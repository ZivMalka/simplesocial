"""simplesocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r'^user/', include('accounts.urls')),
    url(r"^posts/", include('posts.urls', namespace='posts')),
    url(r"^groups/", include('groups.urls', namespace='groups')),
    url(r"^activities/", include('activities.urls', namespace='activities')),
    url(r"^nutrition/", include('nutrition.urls', namespace='nutrition')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
