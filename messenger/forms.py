from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class ComposeForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={"class": "input", 'placeholder' : "Write your message...", }) ,label='')