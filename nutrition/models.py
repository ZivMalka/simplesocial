from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.exceptions import ValidationError
User = get_user_model()

def no_future(value):
    today = date.today()
    if value < today:
        raise ValidationError('Date has passed.')



class Plan(models.Model):
    '''plan model'''
    class Meta:
        ordering = ['date']

    user = models.ForeignKey(User, related_name="nutrition", on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=40)
    date = models.DateField(help_text="Enter date", validators=[no_future])

    def __str__(self):
        return self.subtitle

    def get_absolute_url(self):
        '''
        Returns the canonical URL to view this object
        '''
        return reverse('nutrition:detail', kwargs={'plan_id': self.id})


    def get_energy_value(self):
        x = Nutrition.get_energy_value(self.id)
        return x

class Nutrition(models.Model):
    '''Nutrition class'''
    class Meta:
        ordering = ['time']
        get_latest_by = ['time']
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    time = models.TimeField(null=True, blank=True)
    description = models.TextField()
    amount = models.IntegerField()
    energy = models.FloatField()


    def __str__(self):
        return self.description

    def get_owner_object(self):
        '''
        Returns the object that has owner information
        '''
        return self.plan

    def get_energy_value(self):
        '''calc the calories in the menu'''
        plan = get_object_or_404(Plan, pk=self)
        sum = 0
        for cal in plan.nutrition_set.all():
            sum = sum + cal.energy
        return int(float(sum))













