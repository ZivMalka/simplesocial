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


def appoint(request, username):
    if request.user.username == username or request.user.is_superuser:
        now = datetime.now()


        upcoming_events =  Appointment.objects.filter(date__gt = now).order_by('date', 'time')
        previous_events = Appointment.objects.filter(date__lte=now).order_by('date', 'time')

        list_upcoming = []
        for app in upcoming_events:
            if app.user == request.user or app.sender == request.user:
                list_upcoming.append(app)

        list_previous = []
        for app in previous_events:
            if app.user == request.user or app.sender == request.user:
                list_previous.append(app)

        return render(request, 'appointment.html', {"previous_events" : list_previous, "upcoming_events": list_upcoming})

def create_event(request):
    if request.user.is_superuser:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            task = form.cleaned_data.get('task')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            Appointment.objects.create(user=user, task=task, time=time, date=date, sender=request.user)
            messages.success(request, 'Appointment Added!')
            return HttpResponseRedirect(reverse("appointments:appoint", kwargs={"username": request.user.username}))

        context = {'form': form}
        return render(request, 'create_event.html', context)

def delete_event(request, appoint_id, username):
    if request.user.is_superuser:
        appointment = Appointment.objects.get(pk=appoint_id)
        appointment.delete()
        return appoint(request, username)


def edit_event(request, appointment_id, username):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event Updated Successfully')
        return HttpResponseRedirect(reverse("appointments:appoint", kwargs={"username": request.user.username}))
    return render(request, 'edit_event.html', {'form': form})



