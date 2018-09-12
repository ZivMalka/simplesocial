from django.shortcuts import render, redirect
from .forms import WorkoutForm, SetForm
from django.shortcuts import get_object_or_404
from workout.models import Workout, Set
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from notify.signals import notify
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

def add_workout(request, username):
    """
    New workout plan
    :param request:
    return
    """
    if request.user.is_superuser:
        form = WorkoutForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(username=username)
            day = form.cleaned_data.get('day')
            title = form.cleaned_data.get('title')
            date = form.cleaned_data.get('creation_date')
            workout = Workout.objects.create(user=user, day=day, title=title, creation_date=date)
            notify.send(request.user, recipient=workout.user, actor=request.user, verb='Added a new workout.',
                        nf_type='plan_by_one_user', target=workout)
            messages.success(request, 'Workout Day Added!')
            return HttpResponseRedirect(reverse("workout:overview", kwargs={"username": workout.user.username}))
        context = {
            "form": form,
        }

        return render(request, 'workout/add_workout.html', context)
    else:
        return HttpResponse("Only authorized user can add workout plans")

    return redirect('/')

def add_set(request, workout_id):
    """
    add new set to workout
    :param request:
    :param workout_id:
    :return HttpResponse redirect to set list
    """
    if request.user.is_superuser:
        form = SetForm(request.POST or None)
        workout = get_object_or_404(Workout, pk=workout_id)
        if form.is_valid():
            workouts_sets = workout.set_set.all()
            for s in workouts_sets:
                if s.exercise == form.cleaned_data.get("exercise"):
                    context = {
                        'workout': workout,
                        'form': form,
                        'error_message': 'You already added that excersice',
                    }
                    return render(request, 'workout/add_set.html', context)
            set = form.save(commit=False)
            set.workout = workout
            messages.success(request, 'Exercise Added!')
            set.save()
            return HttpResponseRedirect(reverse("workout:view", kwargs={'workout_id': workout.id}))

        context = {
            'workout': workout,
            'form': form,
        }
        return render(request, 'workout/add_set.html', context)


def delete_workout(request, workout_id, username):
    '''delete workout plan'''
    if request.user.is_superuser:
        workout = Workout.objects.get(pk=workout_id)
        workout.delete()
        return redirect('workout:work_list_manage', username)


def delete_set(request, workout_id, set_id):
    '''delete'''
    if request.user.is_superuser:
        workout = get_object_or_404(Workout, pk=workout_id)
        set = Set.objects.get(pk=set_id)
        set.delete()
        return render(request, 'workout/view.html', {'workout': workout})


def view(request, workout_id):
        workout = get_object_or_404(Workout, pk=workout_id)
        user = workout.user
        return render(request, 'workout/view.html', {'workout': workout, 'user': user})


from django.db.models import Q

def overview(request, username):
    '''return all workouts of the user'''
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        if Workout.objects.filter(user=user):
            weekly = (Workout.objects.latest('creation_date'))
            workouts = Workout.objects.filter(Q(user=user) & ~Q(id=weekly.id))
        else:
            return render(request, 'workout/overview.html')
        return render(request, 'workout/overview.html', {'workouts': workouts, 'user': user, 'weekly':weekly})


def edit_set(request,workout_id , set_id, username):
        workout = get_object_or_404(Workout, pk=workout_id)
        set = get_object_or_404(Set, pk=set_id)
        if request.method == "POST":
            form = SetForm(request.POST, instance=set)
            try:
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Your Set Has Been Updated')
                    return render(request, 'workout/view.html', {'workout': workout}, username)
            except Exception as e:
                messages.warning(request, 'Your set was not saved due to an error: {}'.format(e))
        else:
            form = SetForm(instance=set)
        context = {
            'form': form,
            'workout': workout,
        }
        return render(request, 'workout/edit_set.html', context)



def edit_workout(request, workout_id, username):
    """

    :param request:
    :param workout_id:
    :param username:
    :return:
    """
    workout = get_object_or_404(Workout, pk=workout_id)
    form = WorkoutForm(request.POST or None, instance=workout)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your Workout Day Has Been Updated')
        return redirect('workout:work_list_manage', username)
    return render(request, 'workout/edit_workout.html', {'form': form})

def work_list_manage(request, username):
        '''return the list of workout of user in the manage control'''
        user = User.objects.get(username=username)
        workouts = Workout.objects.filter(user=user)
        return render(request, 'workout/work_list_manage.html', {'workouts': workouts, 'user':user})


