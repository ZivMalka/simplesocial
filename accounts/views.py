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
from accounts.fusioncharts import FusionCharts
from accounts.forms import FilterDate

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


def get_users(request):
    users = User.objects.all()
    return render (request, 'accounts/users.html', {'users':users})

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
def personal_profile(request, username):
    if request.user.username == username:
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        content1 = chart(request, username)
        content2 = chart_bodyfat(request, username, None)
        if (user_P.height is None or user_P.current_weight is None):
            bmi = "Empty"
        else:
            bmi = (user_P.current_weight) / (user_P.height) ** 2
        return render(request, 'accounts/personal_profile.html', {"user":user, 'bmi': bmi,'output':content1, 'output2':content2 })
    else:
        return HttpResponse("No access to this page")

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
                timestamp = form.cleaned_data.get('timestamp')

                p1 = WeightList(weight=weight, body_fat=body_fat, timestamp=timestamp)
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

# Loading Data from a Static JSON String
# Example to create a Column 2D chart with the chart data passed in JSON string format.
# The `fc_json` method is defined to load chart data from a JSON string.
# **Step 1:** Create the FusionCharts object in a view action

def myconverter(o):
    return "{}-{}-{}".format(o.year, o.month, o.day)


def myconverter_month(o):
    return "{}".format(o.month)

def myconverter_year(o):
    return "{}".format(o.year)

# The `chart` function is defined to generate Column 2D chart from database.
def chart(request, username):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {

    }
    dataSource['chart'] = {
        "caption": "Weight lost",
        "subCaption": "Weight lost",
        "xAxisName": "Month",
        "yAxisName": "Weight (In Kg)",
        "numberPrefix": "kg",
        "theme": "zune",
        "canvasBorderColor": "'666666",
        "canvasBorderThickness": "4",
        "canvasBorderAlpha": "80",
        "canvasbgColor": "#1790e1",
        "canvasbgAlpha": "10",
        "canvasBorderThickness": "1",
        "showAlternateHGridColor": "0",
        "bgColor": "#eeeeee",
        "color": "#6baa01",

    }
    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.
    form = FilterDate(request.POST, instance=request.user.userprofileinfo)
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    if request.user.username == username:
        username = request.user.username
        user = User.objects.get(username=username)

        #filter by date
        if request.method == 'POST':

            form = FilterDate(request.POST, instance=request.user.userprofileinfo)
            if form.is_valid():
                date = form.cleaned_data.get('timestamp')
                month = myconverter_month(date)
                year = myconverter_year(date)
                content = chart_bodyfat(request, username, date)

                for key in UserProfileInfo.objects.filter(user=user):
                    # for key in user.userprofileinfo.weight_history.all():
                    for k in key.weight_history.filter(timestamp__month=month, timestamp__year=year):
                        data = {}
                        #  date = json.dumps(key.timestamp, default = myconverter)
                        #  date = json.dumps(date)
                        data['label'] = myconverter(k.timestamp)
                        data['value'] = k.weight
                        data['color']= "#9b59b6"
                        dataSource['data'].append(data)
                    # Create an object for the Column 2D chart using the FusionCharts class constructor
                column2D = FusionCharts("line", "ex1", "600", "350", "chart-1", "json", dataSource)
                return render(request, 'accounts/personal_profile.html',
                              {'output': column2D.render(), 'output2':content})

        for key in user.userprofileinfo.weight_history.all():
            data = {}
            #  date = json.dumps(key.timestamp, default = myconverter)
            #  date = json.dumps(date)
            data['label'] = myconverter(key.timestamp)
            data['value'] = key.weight
            dataSource['data'].append(data)
            data['color']=  "#9b59b6"
        # Create an object for the Column 2D chart using the FusionCharts class constructor
        column2D = FusionCharts("line", "ex1", "600", "350", "chart-1", "json", dataSource)
        return (column2D.render())



def chart_bodyfat(request, username, date):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Body Fat Lost",
        "subCaption": "--",
        "xAxisName": "Month",
        "yAxisName": "Body Fat (In %)",
        "numberPrefix": "%",
        "theme": "zune"
    }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    if request.user.username == username:
        username = request.user.username
        user = User.objects.get(username=username)

        if date is None:
            for key in user.userprofileinfo.weight_history.all():
                data = {}
                #  date = json.dumps(key.timestamp, default = myconverter)
                #  date = json.dumps(date)
                data['label'] = myconverter(key.timestamp)
                data['value'] = key.body_fat
                data['color'] = "#6baa01"
                dataSource['data'].append(data)

            # Create an object for the Column 2D chart using the FusionCharts class constructor
            column2D = FusionCharts("line", "ex2", "600", "350", "chart-2", "json", dataSource)
            return (column2D.render())

        month = myconverter_month(date)
        year = myconverter_year(date)
        for key in UserProfileInfo.objects.filter(user=user):
            # for key in user.userprofileinfo.weight_history.all():
            for k in key.weight_history.filter(timestamp__year=year, timestamp__month=month):
                data = {}
                #  date = json.dumps(key.timestamp, default = myconverter)
                #  date = json.dumps(date)
                data['label'] = myconverter(k.timestamp)
                data['value'] = k.body_fat
                data['color'] = "#6baa01"
                dataSource['data'].append(data)
            # Create an object for the Column 2D chart using the FusionCharts class constructor
        column2D = FusionCharts("line", "ex2", "600", "350", "chart-2", "json", dataSource)
        return (column2D.render())
    #   username = request.user.username

def chart_filter(request, username):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Weight lost",
        "subCaption": "Weight lost",
        "xAxisName": "Month",
        "yAxisName": "Weight (In Kg)",
        "numberPrefix": "kg",
        "theme": "zune"
    }
    string = "weight"
    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.
    dataSource['data'] = []

    if request.user.username == username:
        username = request.user.username
        user = User.objects.get(username=username)
        content2 = chart_bodyfat(request, username)
        if request.method == 'POST':
            form = FilterDate(request.POST, instance=request.user.userprofileinfo)
            if form.is_valid():
                date = form.cleaned_data.get('timestamp')
                month = myconverter_month(date)
                year = myconverter_year(date)
                for key in UserProfileInfo.objects.filter(user=user):
                    # for key in user.userprofileinfo.weight_history.all():
                    for k in key.weight_history.filter(timestamp__month=month, timestamp__year=year):
                        data = {}
                        #  date = json.dumps(key.timestamp, default = myconverter)
                        #  date = json.dumps(date)
                        data['label'] = myconverter(k.timestamp)
                        data['value'] = k.weight
                        dataSource['data'].append(data)
                    # Create an object for the Column 2D chart using the FusionCharts class constructor
                column2D = FusionCharts("line", "ex1", "600", "350", "chart-1", "json", dataSource)
                return render(request, 'accounts/personal_profile.html', {'output': column2D.render(),'output2':content2, 'form': form})
            return HttpResponseRedirect(reverse("accounts:personal_profile", kwargs={"username": user.username}))

