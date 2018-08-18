from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfileInfo, WeightList
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from django.forms.fields import DateField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['profile_pic']

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class UserPersonalProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('height','body_fat','birth_date','current_weight')

class WeightHistoryForm(forms.ModelForm):
    weight = forms.FloatField(required=True, min_value=30)
    body_fat = forms.FloatField(required=True, min_value=5)
    timestamp = forms.FloatField(required=True)

    class Meta:
        model = WeightList
        fields = ('weight' , 'body_fat', 'timestamp')
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'class': 'datepicker'})
        }

class FilterDate(forms.ModelForm):
    class Meta:
        model = WeightList
        fields = ('timestamp', )
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'class': 'datepicker'})
        }