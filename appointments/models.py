from django.db import models
from django.contrib.auth.models import User



class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="appointment", on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):

        return self.task
