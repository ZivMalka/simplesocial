from accounts.forms import UserForm, UserProfileInfoForm,  EditProfileForm, UserPersonalProfileInfoForm, WeightHistoryForm
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
from .models import UserProfileInfo, WeightList
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from groups.models import GroupMember

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
        return HttpResponse("No access to this page")


@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        user2 = UserProfileInfo.objects.get(user=user)
        p1 = WeightList(weight='50')
        p1.save()
        user2.weight_history.add(p1)
        for obj in user2.weight_history.all():
            print(obj.weight)

        return render(request, 'accounts/profile.html', {"user":user})

@login_required
def personal_profile(request, username):
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        if (user_P.height is None or user_P.current_weight is None):
            bmi = "Empty"
        else:
            bmi = (user_P.current_weight) / (user_P.height) ** 2
        return render(request, 'accounts/personal_profile.html', {"user":user, 'bmi': bmi})

@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        my_groups = GroupMember.objects.filter(user=user)
        url = reverse("posts:for_user",  kwargs={"username": user.username})
        return render(request, 'accounts/profile.html', {"user":user, 'my_groups': my_groups, 'url':url })



@login_required
def edit_personal_profile(request, username):
    if request.user.is_superuser:
        if request.method == 'POST':
            profile_form = UserPersonalProfileInfoForm(request.POST, instance=request.user.userprofileinfo)

            if profile_form.is_valid():
                weight = profile_form.cleaned_data.get('current_weight')

                profile = profile_form.save()
                #profile = profile_form.save(commit=False)
                profile.save()

                if weight is not None:
                    p1 = WeightList(weight=weight)
                    p1.save()
                    user = User.objects.get(username=username)
                    user_P = UserProfileInfo.objects.get(user=user)
                    user_P.weight_history.add(p1)

                messages.success(request, 'Your personal profile was successfully updated!')
                return HttpResponseRedirect(reverse("accounts:personal_profile", kwargs={"username": user.username}))

        else:

            profile_form = UserPersonalProfileInfoForm(request.POST, instance=request.user.userprofileinfo)

            return render(request, 'accounts/personal_profile_edit.html',
                          {'profile_form': profile_form})
    else:
        return HttpResponse("No access to this page")


def delete_weight(request, pk):
    user = User.objects.get(username=request.user.username)
    user_P = UserProfileInfo.objects.get(user=user)
#    d = WeightList.objects.filter(weight_list__user_id=user.id, weight=weight, timestamp=date)
    d= WeightList.objects.get(id=pk)
    d.delete()
    return HttpResponseRedirect(reverse("accounts:personal_profile", kwargs={"username": user.username }))



def add_weight(request, username):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = WeightHistoryForm(request.POST, instance=request.user.userprofileinfo)

            if form.is_valid():
                weight = form.cleaned_data.get('weight')
                body_fat = form.cleaned_data.get('body_fat')


                p1 = WeightList(weight=weight, body_fat=body_fat)
                p1.save()
                user = User.objects.get(username=username)
                user_P = UserProfileInfo.objects.get(user=user)
                user_P.weight_history.add(p1)
                return HttpResponseRedirect(reverse("accounts:personal_profile", kwargs={"username": user.username}))

        else:
            form = WeightHistoryForm(request.POST, instance=request.user.userprofileinfo)
            return render(request, 'accounts/add_weight.html', {'form': form})
    else:
            return HttpResponse("No access to this page")

def get_groups(request, username):
    user = User.objects.get(username=request.user.username)
    my_groups = GroupMember.objects.filter(user=user)
    args = {'my_groups' : my_groups}
    return render (request, 'accounts/profile.html', args)