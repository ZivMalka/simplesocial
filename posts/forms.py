from django import forms
from .models import Post
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea


class PostForm(forms.ModelForm):


  message = forms.CharField(widget=EmojiPickerTextarea, label='')
  post_pic = forms.ImageField(label='', required=False)

  class Meta:
        model = Post
        fields = ('message', 'post_pic',)