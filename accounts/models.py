from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class WeightList(models.Model):
    """
    Save all weight data
    """

    class Meta:
        ordering = ['timestamp']

    weight = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    body_fat = models.FloatField(null=True, blank=True)


#Extands User model of django
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    description = models.CharField(null=True, blank=True, max_length=250)
    birth_date = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    body_fat = models.FloatField(null=True, blank=True)
    current_weight = models.FloatField(null=True, blank=True)
    weight_history = models.ManyToManyField(WeightList, blank=True, related_name='weight_list')


    def create_user_profile(sender, instance, created, **kwargs):
        """
            Create User profile
        """
        if created:
            user_profile = UserProfileInfo.objects.create(user=instance)

    def get_redirect_url(self):
        """
        reverse to profile page
        """
        return reverse("accounts:profile",kwargs={"username": self.user.username})

    post_save.connect(create_user_profile, sender=User)

    def get_absolute_url(self):
        return reverse("accounts:profile",kwargs={"username": self.user.username})

    def __str__(self):
        '''return user obj'''
        return self.user.username



