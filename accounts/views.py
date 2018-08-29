from h5py.h5 import H5PYConfig

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
from nutrition.models import Nutrition, Plan
import json
from datetime import datetime, time
import math
from posts.models import Post
from activities.models import Comment
from groups.models import Group,GroupMember
from django.contrib.auth.mixins import LoginRequiredMixin


def manager_control(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'manager_control.html', {'users': users})
    else:
        return redirect('/')


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,email=email)
            user = authenticate(username=username, password=password)
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


def upload_pic(request):

    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_pic' in request.FILES:
                form.profile_pic = request.FILES['profile_pic']

            m = get_object_or_404(UserProfileInfo, user=request.user)
            m.profile_pic = form.cleaned_data['profile_pic']
            m.save()
            return HttpResponseRedirect(reverse("accounts:profile", kwargs={"username": request.user.username}))
        else:
            form = UserProfileInfoForm(request.POST, request.FILES)
            return render(request, 'accounts/profile.html',{'form': form})

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
            user_form_edit = EditProfileForm(instance=request.user)
            profile_form = UserProfileInfoForm(instance=request.user.userprofileinfo)
            return render(request, 'accounts/edit_profile.html',
                          {'user_form_edit': user_form_edit, 'profile_form': profile_form})
    else:
        return HttpResponse("No access to this page")

def chart_visualsion(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        if request.method == 'POST':
            form = FilterDate(request.POST, instance=request.user.userprofileinfo)
            if form.is_valid():
                date = form.cleaned_data.get('timestamp')
                month = myconverter_month(date)
                year = myconverter_year(date)
                list = user.userprofileinfo.weight_history.filter(timestamp__year=year, timestamp__month=month)
                plans = Plan.objects.filter(user=user, date__month=month, date__year=year)


        elif request.GET.get('year'):
            year = (request.GET.get('year'))
            list = user.userprofileinfo.weight_history.filter(timestamp__year=year)
            plans = Plan.objects.filter(user=user, date__year=year)
            month = None


        else:
            date = datetime.now()
            month = myconverter_month(date)
            year = myconverter_year(date)
            plans = Plan.objects.filter(user=user, date__month=month, date__year=year)
            list = user.userprofileinfo.weight_history.filter(timestamp__year=year, timestamp__month=month)

        content1 = chart(request, list)
        content2 = chart_bodyfat(request, list)
        content3 = chart_calories(request, plans)
        content4 = WeightLossPercentage(request, username)
        content5=weight_lossDistrbotion(request, username)
        content6=activity_log_chart(request, username)
        content7 = activity_log_all(request, month, year)
        return render(request, 'accounts/Graph.html',
                      {"user": user, 'output': content1, 'output2': content2, 'output3': content3,
                       'output4': content4, 'output5': content5, 'output6': content6, 'output6': content6,'output7': content7})

    else:
        return HttpResponseRedirect(reverse("accounts:profile", kwargs={"username": request.user.username}))

def calc_bmi(user_P):
    if (user_P.height is None or user_P.current_weight is None):
        bmi = "Empty"
    else:
        bmi = round((user_P.current_weight) / (user_P.height) ** 2, 2)
    return bmi

@login_required
def personal_profile(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        bmi = calc_bmi(user_P)
        return render(request, 'accounts/personal_profile.html', {"user":user, 'bmi': bmi })
    else:
        return HttpResponse("No access to this page")


@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        my_groups = GroupMember.objects.filter(user=user)
        my_post  = Post.objects.filter(user=user)
        url = reverse("posts:for_user",  kwargs={"username": user.username})
        return render(request, 'accounts/profile.html', {"user":user, 'my_groups': my_groups, 'url':url, 'my_post':my_post  })



@login_required
def edit_personal_profile(request, username):
    if request.user.is_superuser:
        if request.method == 'POST':
            profile_form = UserPersonalProfileInfoForm(request.POST, instance=request.user.userprofileinfo)

            if profile_form.is_valid():
                weight = profile_form.cleaned_data.get('current_weight')
                body_fat = profile_form.cleaned_data.get('body_fat')
                profile = profile_form.save()
                #profile = profile_form.save(commit=False)
                profile.save()

                if weight is not None:
                    p1 = WeightList(weight=weight, timestamp=datetime.now(), body_fat=body_fat)
                    p1.save()
                    user = User.objects.get(username=username)
                    user_P = UserProfileInfo.objects.get(user=user)
                    user_P.weight_history.add(p1)

                messages.success(request, 'Your personal profile was successfully updated!')
                return HttpResponseRedirect(reverse("accounts:perosnal_profile", kwargs={"username": request.user.username}))
        else:
            profile_form = UserPersonalProfileInfoForm(request.POST, instance=request.user.userprofileinfo)
            return render(request, 'accounts/personal_profile_edit.html',
                          {'profile_form': profile_form})
    else:
        return HttpResponse("No access to this page")


def delete_weight(request, pk, username):
    user = User.objects.get(username=username)
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
                user_P.current_weight =  user_P.weight_history.latest('timestamp').weight
                user_P.body_fat = user_P.weight_history.latest('timestamp').body_fat
                user_P.save()
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
def chart(request, list):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {
    }
    dataSource['chart'] = {
        "caption": "Weight loss",
        "xAxisName": "Month",
        "yAxisName": "Weight (In Kg)",
        "numberPrefix": "kg",
        "setadaptiveymin": "1",
        "theme": "fint",
    }
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    for k in list:
                data = {}
                data['label'] = myconverter(k.timestamp)
                data['value'] = k.weight
                dataSource['data'].append(data)
                data['color']=  "#9b59b6"
            # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("line", "ex1", "600", "350", "chart-1", "json", dataSource)
    return (column2D.render())



def chart_bodyfat(request, list):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Body Fat Lost",
        "xAxisName": "Month",
        "yAxisName": "Body Fat (In %)",
        "numberPrefix": "%",
        "theme": "fint",

    }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.
    dataSource['data'] = []
    for k in list:
                data = {}
                data['label'] = myconverter(k.timestamp)
                data['value'] = k.body_fat
                data['color'] = "#6baa01"
                dataSource['data'].append(data)
            # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("line", "ex2", "600", "350", "chart-2", "json", dataSource)
    return (column2D.render())



def chart_calories(request, plans):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Calories intake",
        "subCaption": "Calories",
        "xAxisName": "Date",
        "yAxisName": "Total calories per day (In kcal)",
        "numberPrefix": "kcal",
        "bgColor": "#FFFFFF",
        "theme": "fint",
        "palettecolors": "08ee4,9b59b6,6baa01,e44a00"
    }
    dataSource['data'] = []
    for plan in plans:
                data = {}
                data['label'] = myconverter(plan.date)
                data['value'] = ((plan.get_energy_value()))
                dataSource['data'].append(data)
            # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("column2d", "ex3", "600", "350", "chart-3", "json", dataSource)
    return (column2D.render())


def WeightLossPercentage(request, username):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Weight loss Percentage",
        "subCaption": "Weight loss Percentage",
        "yAxisName": "Weight loss Percentage",
        "numberPrefix": "%",
        "setadaptiveymin": "1",
        "theme": "fint",
        "palettecolors": "#FF2DC6,#632289,#FFAE00",
    }
    dataSource['data'] = []
    for user in User.objects.all():
        data = {}
        data['label'] = user.username
        data['value'] = calc_total_loss_per(user, user.userprofileinfo.current_weight)
        dataSource['data'].append(data)
    column2D = FusionCharts("column2d", "ex4", "600", "350", "chart-4", "json", dataSource)
    return (column2D.render())

# Distrbotion
def weight_lossDistrbotion(request, username):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = { }
    dataSource['chart'] = {
        "caption": "Weight loss distribution",
        "subCaption": "Weight loss of all the users",
        "bgColor": "#FFFFFF",
        "theme": "fint",
        "valueFontSize": "15",
        "palettecolors": "#0075c2",
    }
    labels = ["0","1-9", "10-19", "20-29", "30-39", "40-49", "50"]
    negatives =  ["0","-1--9","-10-19","-20--29","-30-39","-40--49","-50"]
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    if request.user.username == username or request.user.is_superuser:
                arr = []
                for user in User.objects.all():
                    index = calc_total_loss_per(user, user.userprofileinfo.current_weight)/10
                    if len(str(abs(index)))<2:
                        arr.append(index)
                    else:
                        index = (math.ceil(calc_total_loss_per(user, user.userprofileinfo.current_weight)/10))
                        arr.append(index)


                for i in range (negatives.__len__()-1, -1,-1):
                    if i==0:
                        continue
                    data = {}
                    data['label'] = negatives[i]
                    data['value'] = arr.count(-i)
                    dataSource['data'].append(data)

                for i in range(0, labels.__len__()):
                    data = {}
                    data['label'] = labels[i]
                    data['value'] = arr.count(i)
                    dataSource['data'].append(data)
                    # Create an object for the Column 2D chart using the FusionCharts class constructor
                column2D = FusionCharts("column2d", "ex5", "600", "350", "chart-5", "json", dataSource)
                return (column2D.render())

# chart activity of Individual user
def activity_log_chart(request, username):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "My activity Log: Group, posts, comments and likes",
        "subCaption": "My monthly activity in social app",
        "xAxisName": "Month",
        "bgColor": "#FFFFFF",
        "theme": "fint",
        "valueFontSize": "15",
        "palettecolors": "#0075c2,#06AF8F,#08F73A",
    }

    dataSource['data'] =[]
    user = User.objects.get(username=username)
    for i in range(1, 13):
            data = {}
            data['label'] = i
            data['value'] = Post.objects.filter(user=user, created_at__month=i).count() + \
                            Post.objects.filter(likes=user,  date_of_like__month=i).count() + \
                            Comment.objects.filter(user=user, timestamp__month=i).count() + \
                            GroupMember.objects.filter(user=user, date__month=i).count()
            dataSource['data'].append(data)
    column2D = FusionCharts("column2d", "ex6", "600", "350", "chart-6", "json", dataSource)
    return (column2D.render())

#chart avtivity of all the users
def activity_log_all(request, month, year):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Activity Log: Posts, comments and likes distribution",
        "xAxisName": "Month",
        "bgColor": "#FFFFFF",
        "theme": "fint",
        "valueFontSize": "15",
        "showlegend": "1",
        "legendposition": "bottom",
    }
    dataSource['data'] =[]
    for user in User.objects.all():
            data = {}
            data['label'] = user.username
            data['value'] = Post.objects.filter(user=user, created_at__month=month, created_at__year=year).count() + \
                            Post.objects.filter(likes=user,  date_of_like__month=month, date_of_like__year=year).count() + \
                            Comment.objects.filter(user=user, timestamp__month=month, timestamp__year=year).count() + \
                            GroupMember.objects.filter(user=user, date__month=month, date__year=year).count()

            dataSource['data'].append(data)
    column2D = FusionCharts("pie2d", "ex7", "600", "350", "chart-7", "json", dataSource)
    return (column2D.render())



from accounts.printing import MyPrint
from io import BytesIO

def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_users()

    response.write(pdf)
    return response

def calc_total_loss(user, current):
    total = 0
    for key in user.userprofileinfo.weight_history.all():
        if total == 0:
           total = current - key.weight
        else:
           break
    return total

def calc_total_loss_per(user, current):
    total = 0
    for k in user.userprofileinfo.weight_history.all():
        if total == 0:
           total = round((((k.weight- current)/k.weight)*100),2)
        else:
           break
    return total


# Reports
from django.http import HttpResponse
from django.views.generic import View
from accounts.printing import render_to_pdf #created in step 4


def generate_reports(request):
    GeneratePdf_of_all_user(request)
    return render(request, 'accounts/reports.html')

import numpy as np
from statistics import mean, stdev, median
from decimal import Decimal as d

def GeneratePdf_of_all_user(request):
    if request.user.is_superuser:
        dataSource = {}
        dataSource['data'] = []
        numbers = []
        for user in User.objects.all():
                data = {}
                data['weight_loss_per'] = calc_total_loss_per(user, user.userprofileinfo.current_weight)
                data['weight_loss']  = calc_total_loss(user, user.userprofileinfo.current_weight)
                data ['user'] = user
                numbers.append(data['weight_loss_per'])
                dataSource['data'].append(data)

        avg = round((mean(numbers)), 2)
        std = round(stdev(numbers), 2)
        med = round(median(numbers), 2)
        numbers.clear()
      #  numbers = {'avg': avg, 'std': std, 'med': med}

        for data in dataSource['data']:
            numbers.append((data.get('weight_loss')))

        avg2 = round((mean(numbers)), 2)
        std2 = round(stdev(numbers), 2)
        med2 = round(median(numbers), 2)

        numbers = {'avg': avg, 'std': std, 'med': med, 'avg2' : avg2, 'std2' : std2, 'med2': med2}

        pdf = render_to_pdf('accounts/all_users_report.html',
                            {'data': dataSource, 'numbers': numbers})

        return HttpResponse(pdf, content_type='application/pdf')

    else:
        return render(request, 'accounts/reports.html')

def  GeneratePdf(request, username):
        user = User.objects.get(username=username)
        dataSource = {}
        dataSource['data'] = []

        if request.method == "POST":
            form = FilterDate(request.POST, instance=request.user.userprofileinfo)
            if form.is_valid():

                time = form.cleaned_data.get('timestamp')
                month = myconverter_month(time)
                year = myconverter_year(time)
                list = user.userprofileinfo.weight_history.filter(timestamp__year=year, timestamp__month=month)
                type  = time
                if not list:

                    return render(request, 'accounts/reports.html')

        elif request.GET.get('year'):
                year = (request.GET.get('year'))
                list = user.userprofileinfo.weight_history.filter(timestamp__year=year)
                type = year
                if not list :
                    return render(request, 'accounts/reports.html')
        else:
                return render(request, 'accounts/reports.html')

        for k in list:
                data = {}
                data['body_fat']= k.body_fat
                data['weight'] = k.weight
                data['timestamp'] = k.timestamp
                current = k.weight
                dataSource['data'].append(data)

        total = calc_total_loss(user, current)
        total_in_per = calc_total_loss_per(user, current)
        bmi = calc_bmi(user.userprofileinfo)
        print(data)
        pdf = render_to_pdf('accounts/pdf_template.html',
                                        {'data': dataSource, 'total': total, 'total_in_per': total_in_per,
                                         'bmi': bmi, 'user': user, 'type': type })

        return HttpResponse(pdf, content_type='application/pdf')



