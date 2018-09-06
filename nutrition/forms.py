from django import forms
from .models import Plan, Nutrition
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms.fields import DateField



class PlanForm(forms.ModelForm):
    date = DateField(widget = AdminDateWidget())
    class Meta:
        model = Plan
        fields = ['subtitle' ,'date']


class NutritionForm(forms.ModelForm):
    time = forms.TimeField(widget= AdminTimeWidget)

    class Meta:
        model = Nutrition
        fields = ['time', 'description', 'amount', 'energy']



