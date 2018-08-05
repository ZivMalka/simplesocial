from django import forms

from .models import Plan, Nutrition


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ['user','subtitle']


class NutritionForm(forms.ModelForm):

    class Meta:
        model = Nutrition
        fields = ['time', 'description', 'amount', 'energy']



