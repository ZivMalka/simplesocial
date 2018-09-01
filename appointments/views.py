from django.shortcuts import render,redirect
from django.contrib import messages
from appointments.models import Appointment
from .forms import AppointmentForm
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.contrib.auth.models import User


# Create your views here.

def appointment_manage(request,username):
    if request.user.is_superuser:
        user = User.objects.get(username=username)
        list = Appointment.objects.filter(user=user)
        now = datetime.now()
        context={
                'events_today' : Appointment.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).order_by('date', 'time'),
                'events_later' : Appointment.objects.filter(date__gt=date.today()).order_by('date', 'time'),
                'list' : list,
        }
        return render(request, 'appointment_manage.html', context)

def appoint(request, username):
    if request.user.username == username or request.user.is_superuser:
        now = datetime.now()
        context={
                'events_today' : Appointment.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).order_by('date', 'time'),
                'events_later' : Appointment.objects.filter(date__gt=date.today()).order_by('date', 'time'),
        }
        return render(request, 'appointment.html', context)

def create_event(request):
    if request.user.is_superuser:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.sender = request.user
            appointment.save()
            messages.success(request, 'Appointment Added!')
            return redirect('appointments:appointment_manage', request.user)
        context = {'form': form}
        return render(request, 'create_event.html', context)



def delete_event(request, appoint_id, username):
    if request.user.is_superuser:
        appointment = Appointment.objects.get(pk=appoint_id)
        appointment.delete()
        return redirect('appointments:appointment_manage', username)


def edit_event(request, appointment_id, username):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event Updated Successfully')
        return redirect('appointments:appointment_manage', username )
    return render(request, 'edit_event.html', {'form': form})
