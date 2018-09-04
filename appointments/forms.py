from django import forms
from .models import Appointment
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms.fields import DateField



class AppointmentForm(forms.ModelForm):
    """
    create Appointment form
    """
    date = DateField(widget = AdminDateWidget())
    time = forms.TimeField(widget= AdminTimeWidget)

    class Meta:

        model = Appointment
        fields = ['user', 'task', 'date', 'time']

