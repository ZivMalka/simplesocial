from .models import Workout, Set
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class WorkoutForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInput)
    class Meta:
        model = Workout
        fields = ['user', 'day', 'title']




class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ['exercise', 'sets', 'reps', 'unit']


