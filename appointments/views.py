from django.shortcuts import render, redirect
from django.contrib import messages
from appointments.models import Appointment
from django.contrib.auth.models import User

from .forms import AppointmentForm
from django.shortcuts import get_object_or_404

# Create your views here.


def appoint(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        appointment = Appointment.objects.filter(user=user)
        return render(request, 'appointment.html', {'appointment': appointment})

def create_event(request):
    if request.user.is_superuser:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.owner = request.user
            appointment = appointment.save()
            appointment = Appointment.objects.filter(user=request.user)
            messages.success(request, 'Appointment Added!')
            return render(request, 'appointment.html', {'appointment': appointment})
        context = {'form': form}
        return render(request, 'create_event.html', context)


def delete_event(request, appoint_id):
    if request.user.is_superuser:
        appointment = Appointment.objects.get(pk=appoint_id)
        appointment.delete()
        appointment = Appointment.objects.filter(user=request.user)
        return render(request, 'appointment.html', {'appointment': appointment})


def edit_event(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request,'Event Updated Successfully')
        appointment = Appointment.objects.filter(user=request.user)
        return render(request, 'appointment.html', {'appointment':appointment} )
    return render(request, 'edit_event.html', {'form': form})

