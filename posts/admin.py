from django.contrib import admin

from . import models
from .models import Post

admin.site.register(models.Post)
