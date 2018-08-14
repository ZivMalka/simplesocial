from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

UNIT = (
    (0, 'Kilometers'),
    (1, 'Reps')
)

class Workout(models.Model):
    class Meta:
        ordering = ["creation_date", ]


    user = models.ForeignKey(User, related_name="workout", on_delete=models.CASCADE)
    creation_date = models.DateField(name='creation_date', auto_now_add=True)
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    title = models.CharField(max_length=15)

    def get_absolute_url(self):

        return reverse('workout:view', kwargs={'workout_id': self.id})

    def __str__(self):

        return self.title


class Set(models.Model):
    '''
    Model for a set of exercises
    '''
    DEFAULT_SETS = 4
    MAX_SETS = 10

    class Meta:
        ordering = ["order", ]

    workout = models.ForeignKey(Workout, name='workout', on_delete=models.CASCADE)
    exercise = models.TextField()
    order = models.IntegerField(blank=True, null=True, name='order')
    sets = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(MAX_SETS)],  default=DEFAULT_SETS)
    reps = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(600)])
    unit = models.IntegerField(choices=UNIT, default=1)


    def __str__(self):

        return self.id

    def get_owner_object(self):
        '''
        Returns the object that has owner information
        '''
        return self.Workout

