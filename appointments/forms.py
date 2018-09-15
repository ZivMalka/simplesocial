from django import forms
from .models import Appointment
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms.fields import DateField
from dal import autocomplete
from django.contrib.auth.models import User
from django.urls import reverse

class AppointmentForm(forms.ModelForm):
    """
    create Appointment form
    """
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=autocomplete.ModelSelect2(url='/appointments/country-autocomplete'))
    date = DateField(widget = AdminDateWidget())
    time = forms.TimeField(widget= AdminTimeWidget)

    class Meta:

        model = Appointment
        fields = ['user', 'task', 'date', 'time']

