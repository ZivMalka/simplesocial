from django.shortcuts import render
from .forms import WorkoutForm, SetForm
from django.shortcuts import get_object_or_404
from workout.models import Workout, Set
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages




def manageView(request):
    workouts = Workout.objects.all()
    return render(request, 'workout/manageView.html', {'workouts': workouts})

def add_workout(request):
    if request.user.is_superuser:
        form = WorkoutForm(request.POST or None)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.save()
            messages.success(request, 'Workout Day Added!')
            return render(request, 'workout/view.html', {'workout': workout})
        context = {
            "form": form,
        }
        return render(request, 'workout/add_workout.html', context)
    else:
        return HttpResponse("Only authorized user can add workout plans")



def add_set(request, workout_id):
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
            return render(request, 'workout/view.html', {'workout': workout})
        context = {
            'workout': workout,
            'form': form,
        }
        return render(request, 'workout/add_set.html', context)


def delete_workout(request, workout_id):
    if request.user.is_superuser:
        workout = Workout.objects.get(pk=workout_id)
        workout.delete()
        workouts = Workout.objects.filter(user=request.user)
        return render(request, 'workout/overview.html', {'workouts': workouts})


def delete_set(request, workout_id, set_id):
    if request.user.is_superuser:
        workout = get_object_or_404(Workout, pk=workout_id)
        set = Set.objects.get(pk=set_id)
        set.delete()
        return render(request, 'workout/view.html', {'workout': workout})


def view(request, workout_id):
        workout = get_object_or_404(Workout, pk=workout_id)
        user = workout.user
        return render(request, 'workout/view.html', {'workout': workout, 'user': user})



def overview(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        workouts = Workout.objects.filter(user=user)
        set_results = Set.objects.all()
        query = request.GET.get("q")
        if query:
            workouts = workouts.filter(
                Q(workout_title__icontains=query)
            ).distinct()
            set_results = set_results.filter(
                Q(set_exercise__icontains=query)
            ).distinct()
            return render(request, 'workout/overview.html', {
                'workouts': workouts,
                'set': set_results,
            })
        else:
            return render(request, 'workout/overview.html', {'workouts': workouts})

<<<<<<< HEAD
def edit_set(request,workout_id , set_id):
        template_name = 'workout/edit_set.html'
        workout = get_object_or_404(Workout, pk=workout_id)
        set = get_object_or_404(Set, pk=set_id)
        if request.method == "POST":
            form = SetForm(request.POST, instance=set)
            try:
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Your Set Has Been Updated')
                    return render(request, 'workout/view.html', {'workout': workout})
            except Exception as e:
                messages.warning(request, 'Your set was not saved due to an error: {}'.format(e))
        else:
            form = SetForm(instance=set)
        context = {
            'form': form,
            'workout': workout,
        }
        return render(request, template, context)
=======
    def edit_set(request,workout_id , set_id):
    template = 'workout/edit_set.html'
    workout = get_object_or_404(Workout, pk=workout_id)
    set = get_object_or_404(Set, pk=set_id)
    if request.method == "POST":
        form = SetForm(request.POST, instance=set)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Exercise Has Been Updated')
                messages.success(request, 'Your Set Has Been Updated')
                return render(request, 'workout/view.html', {'workout': workout})
        except Exception as e:
            messages.warning(request, 'Your set was not saved due to an error: {}'.format(e))
    else:
        form = SetForm(instance=set)
    context = {
        'form': form,
        'workout': workout,
    }
    return render(request, template, context)
>>>>>>> 468fdce40c15aac9f3f4e9a6d570c59744e5b38e

def edit_workout(request, workout_id):
    template = 'workout/edit_workout.html'
    workout = get_object_or_404(Workout, pk=workout_id)
    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Workout Has Been Updated')
                return render(request, 'workout/view.html', {'workout': workout})
        except Exception as e:
            messages.warning(request, 'Your workout was not saved due to an error: {}'.format(e))
    else:
        form = WorkoutForm(instance=workout)
    context = {
        'form': form,
        'workout': workout,
    }
    return render(request, template, context)


