from accounts.forms import UserForm, UserProfileInfoForm,  EditProfileForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import  View, TemplateView, ListView, DeleteView
from django.shortcuts import render
from django.views import generic
from . import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import UserProfileInfo
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
       # profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,email=email)
            user = authenticate(username=username, password=password)

     #       if 'profile_pic' in request.FILES:
      #          profile.profile_pic = request.FILES['profile_pic']

            registered = True

            login(request, user)

            return render(request, 'accounts/signup.html', {'user_form': user_form,'registered': registered})

        else:
            return render(request, 'accounts/signup.html')


    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        return render(request, 'accounts/signup.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'registered': registered})

@login_required
def profile(request):
    args = {'user' : request.user }
    return render(request, 'accounts/profile.html', args)

@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form_edit = EditProfileForm(request.POST, instance=request.user)
            profile_form = UserProfileInfoForm(request.POST, instance=request.user.userprofileinfo)

            if user_form_edit.is_valid() and profile_form.is_valid():
                user = user_form_edit.save()

                user.save()

                profile = profile_form.save(commit=False)

                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')

                return HttpResponseRedirect(reverse("accounts:profile", kwargs={"username": request.user.username}))

        else:
            user_form_edit = EditProfileForm(instance=request.user)
            profile_form = UserProfileInfoForm(instance=request.user.userprofileinfo)

            return render(request, 'accounts/edit_profile.html',
                          {'user_form_edit': user_form_edit, 'profile_form': profile_form})

    else:
        return HttpResponse("no acsses")


@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        return render(request, 'accounts/profile.html', {"user":user})


