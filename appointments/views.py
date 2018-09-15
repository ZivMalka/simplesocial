from django.shortcuts import render,redirect
from django.contrib import messages
from appointments.models import Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.db.models import Q
# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect
from notify.signals import notify



def appoint(request, username):
    '''
    get upcoming apptmein and the past appoitment of the user
    :param request:
    :param username:

    '''
    if request.user.username == username or request.user.is_superuser:
        now = datetime.now()

        upcoming_events =  Appointment.objects.filter(date__gte = now).order_by('date', 'time')
        previous_events = Appointment.objects.filter(date__lt=now).order_by('date', 'time')

        list_upcoming = []
        for app in upcoming_events:
            if app.user == request.user or app.sender == request.user:
                list_upcoming.append(app)

        list_previous = []
        for app in previous_events:
            if app.user == request.user or app.sender == request.user:
                list_previous.append(app)

        return render(request, 'appointment.html', {"previous_events" : list_previous, "upcoming_events": list_upcoming})
    return redirect('/')

def appointment_manage(request):
    if request.user.is_superuser:
        now = datetime.now()
        upcoming_events = Appointment.objects.filter(date__gte=now).order_by('date', 'time')
        previous_events = Appointment.objects.filter(date__lt=now).order_by('date', 'time')

        return render(request, 'appointment_manage.html', {"previous_events" : previous_events, "upcoming_events": upcoming_events})
    return redirect('/')

def create_event(request):
    """
    create an event from admin to user
    :param request:

    """
    if request.user.is_superuser:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            task = form.cleaned_data.get('task')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            app = Appointment.objects.create(user=user, task=task, time=time, date=date, sender=request.user)
            notify.send(request.user, recipient=app.user, actor=request.user, verb='Added a new Meeting.',
                        nf_type='app_by_one_user', target=app)
            messages.success(request, 'Appointment Added!')
            return redirect("appointments:appointment_manage")

        context = {'form': form}
        return render(request, 'create_event.html', context)
    return redirect('home')

def delete_event(request, appoint_id, username):
    '''delete'''
    if request.user.is_superuser:
        appointment = Appointment.objects.get(pk=appoint_id)
        appointment.delete()
        return appointment_manage(request)


def edit_event(request, appointment_id, username):
    '''edit'''
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event Updated Successfully')
        return redirect("appointments:appointment_manage")
    return render(request, 'edit_event.html', {'form': form})



