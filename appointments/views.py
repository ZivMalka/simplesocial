from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from datetime import date
from django.db.models import Q
from .models import User, Appointment
from .forms import AppointmentForm
from django.views.generic.edit import CreateView

# Create your views here.


def appoint(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        appointment = Appointment.objects.filter(user=user)
        query = request.GET.get("q")
        if query:
            appointment = appointment.filter(
                Q(task__icontains=query) |
                Q(date_icontains=query)
            ).distinct()
            return render(request, 'appointment.html', {
                    'appointment': appointment,
            })
        else:
            return render(request, 'appointment.html', {'appointment': appointment})

def create_event(request):
    form = AppointmentForm(request.POST, )
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
