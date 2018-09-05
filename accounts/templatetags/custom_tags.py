import datetime
from django import template
from django.contrib.auth.models import User
register = template.Library()
from accounts.views import calc_total_loss_per
from statistics import mean, stdev, median

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

