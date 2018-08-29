from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from .models import Plan, Nutrition


class PlanForm(forms.ModelForm):
    date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={"id": "datepicker"}))
    class Meta:
        model = Plan
        fields = ['user','subtitle' ,'date']


class NutritionForm(forms.ModelForm):
    time = forms.TimeField(widget= AdminTimeWidget)

    class Meta:
        model = Nutrition
        fields = ['time', 'description', 'amount', 'energy']



