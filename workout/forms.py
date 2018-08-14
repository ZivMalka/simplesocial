from .models import Workout, Set
from django import forms


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['user', 'day', 'title']




class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ['exercise', 'sets', 'reps', 'unit']


