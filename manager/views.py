from django.shortcuts import render
from django.contrib.auth.models import User
from workout.models import Workout
from nutrition.models import Plan
from django.db.models import Q
from django.core.paginator import Paginator


def manager_control(request):
        users = User.objects.all()
        return render(request, 'manager_control.html', {'users': users})

def plan_list(request, username):
        user = User.objects.get(username=username)
        plans = Plan.objects.filter(user=user)
        return render(request, 'plan_list.html', {'plans': plans})

def work_list(request, username):
        user = User.objects.get(username=username)
        workouts = Workout.objects.filter(user=user)
        return render(request, 'work_list.html', {'workouts': workouts})


