from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfileInfo, WeightList
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.fields import DateField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

#Create new user form
class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

#Upload profile pic
class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['profile_pic']

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserPersonalProfileInfoForm(forms.ModelForm):
    birth_date = forms.DateTimeField(required= True,widget=forms.TextInput(attrs={"id": "datepicker", },  ))
    height = forms.FloatField(min_value = 1.40, max_value=2, required= True)
    class Meta:
        model = UserProfileInfo
        fields = ('height','birth_date', 'goal')

class WeightHistoryForm(forms.ModelForm):
    weight = forms.FloatField(required=True, min_value=40, widget=forms.TextInput(attrs={'required': 'true'}),)
    body_fat = forms.FloatField(required=True, min_value=8, widget=forms.TextInput(attrs={'required': 'true'}),)
    timestamp = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={"id": "datepicker"}))
    class Meta:
        model = WeightList
        fields = ('weight' , 'body_fat', 'timestamp')

#FILTER DATE
class FilterDate(forms.ModelForm):
    timestamp = DateField(widget=AdminDateWidget(), )
    class Meta:
        model = WeightList
        fields = ('timestamp', )
