from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum


User = get_user_model()


class Plan(models.Model):

    class Meta:
        ordering = ['date']

    user = models.ForeignKey(User, related_name="nutrition", on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=40)
    date = models.DateField(name='date', auto_now_add=True)

    def __str__(self):
        return self.subtitle

    def get_absolute_url(self):
        '''
        Returns the canonical URL to view this object
        '''
        return reverse('nutrition:detail', kwargs={'plan_id': self.id})
    @staticmethod
    def get_energy_value():

        x = Nutrition.get_energy_value()
        return x

class Nutrition(models.Model):

    class Meta:
        ordering = ['time']
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    time = models.TimeField(null=True, blank=True)
    description = models.TextField()
    amount = models.IntegerField()
    energy = models.DecimalField(max_digits=6 , decimal_places=2)

    def __str__(self):
        return self.description

    def get_owner_object(self):
        '''
        Returns the object that has owner information
        '''
        return self.plan

    @staticmethod
    def get_energy_value():
        value = Nutrition.objects.aggregate(sum=Sum('energy'))['sum']

        return value












