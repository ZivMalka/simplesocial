from django import forms
from .models import Group
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class GroupForm(forms.ModelForm):

  name = forms.CharField(widget=EmojiPickerTextInput)
  description = forms.CharField(widget=EmojiPickerTextarea)

  class Meta:
        model = Group
        fields = ("name", "description")