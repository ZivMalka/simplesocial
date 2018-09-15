from .models import Workout, Set
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms.fields import DateField

class WorkoutForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInput)
    creation_date = DateField(widget = AdminDateWidget(), )
    class Meta:
        model = Workout
        fields = ['title' , 'creation_date']




class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ['day','exercise', 'sets', 'reps', 'unit']
