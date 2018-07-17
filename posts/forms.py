from django import forms
from .models import Post



class PostForm(forms.ModelForm):

   # group = forms.CharField(widget=forms.HiddenInput)
  #  object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
#    content = forms.CharField(label='', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('message',)