from django import forms
from .models import Comment

from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea
class CommentForm(forms.ModelForm):

 #   content_type = forms.CharField(widget=forms.HiddenInput)
  #  object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
#    content = forms.CharField(label='', widget=forms.Textarea)
    short_text = forms.CharField(widget=EmojiPickerTextInput)
    class Meta:
        model = Comment
        fields = ('content',)

