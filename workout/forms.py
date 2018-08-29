from .models import Workout, Set
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class WorkoutForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInput)
    creation_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={"id": "datepicker"}))
    class Meta:
        model = Workout
        fields = ['user', 'day', 'title' , 'creation_date']




class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ['exercise', 'sets', 'reps', 'unit']


