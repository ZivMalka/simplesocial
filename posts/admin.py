from django.contrib import admin

from . import models
from .models import Post, Like

admin.site.register(models.Post)
admin.site.register(models.Like)