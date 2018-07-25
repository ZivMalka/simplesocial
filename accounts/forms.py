from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfileInfo, WeightList
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['profile_pic', 'description']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserPersonalProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('height','body_fat','birth_date','current_weight')

class WeightHistoryForm(forms.ModelForm):
    weight = forms.FloatField(required=True)
    body_fat = forms.FloatField(required=True)
    class Meta:
        model = WeightList
        fields = ('weight' , 'body_fat')