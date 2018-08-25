from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from .models import Plan, Nutrition


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ['user','subtitle']


class NutritionForm(forms.ModelForm):
    time = forms.TimeField(widget= AdminTimeWidget)

    class Meta:
        model = Nutrition
        fields = ['time', 'description', 'amount', 'energy']



