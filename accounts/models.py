
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField
    height = models.DecimalField

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfileInfo.objects.create(user=instance)


    post_save.connect(create_user_profile, sender=User)

    def __str__(self):
        return self.user.username
