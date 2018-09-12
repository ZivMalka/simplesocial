import datetime
from django import template
from django.contrib.auth.models import User
register = template.Library()
from accounts.views import calc_bmi
from statistics import mean, stdev, median

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def bmi(format_string):
    bmi = []
    for user in User.objects.all():
        bmi.append(calc_bmi(user.userprofileinfo))
    if bmi.__len__()>1:
        avg_bmi = mean(bmi)
    else:
        avg_bmi = bmi
    return avg_bmi