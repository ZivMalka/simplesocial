from django.views.generic import TemplateView
from posts.models import Post
from django.shortcuts import render
from braces.views import SelectRelatedMixin
from django.views import generic
from posts import models
from accounts.fusioncharts import FusionCharts
from django.http import HttpResponse
from accounts.models import WeightList, UserProfileInfo, User
import json
from django.shortcuts import redirect



class HomePage(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")

