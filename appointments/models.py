from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Q

def no_future(value):
    today = date.today()
    if value < today:
        raise ValidationError('Date has passed.')





class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="appointment", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    task = models.CharField(max_length=255)
    date = models.DateField(help_text="Enter date", validators=[no_future])
    time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):

        return self.task

