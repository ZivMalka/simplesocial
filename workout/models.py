from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from datetime import date
from django.core.exceptions import ValidationError
User = get_user_model()

def no_future(value):
    today = date.today()
    if value < today:
        raise ValidationError('Date has passed.')
        
        


UNIT = (
    (0, 'Kilometers'),
    (1, 'Reps')
)

class Workout(models.Model):
    '''workout class'''
    class Meta:
        ordering = ["creation_date", ]

    user = models.ForeignKey(User, related_name="workout", on_delete=models.CASCADE)
    creation_date = models.DateField(help_text="Enter date", validators=[no_future])
    title = models.CharField(max_length=15, unique=True)


    def __str__(self):
        return self.title


    def get_absolute_url(self):

        return reverse('workout:view', kwargs={'workout_id': self.id})


DAYS_OF_WEEK = (
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)

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
    day = models.CharField(choices=DAYS_OF_WEEK, default='1', max_length=20)

    def __str__(self):
        return self.get_day_display()



    def get_owner_object(self):
        '''
        Returns the object that has owner information
        '''
        return self.Workout

