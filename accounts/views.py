from accounts.forms import UserProfileInfoForm,  EditProfileForm, \
    UserPersonalProfileInfoForm, WeightHistoryForm, FilterDate, UserCreateForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import UserProfileInfo, WeightList
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from accounts.fusioncharts import FusionCharts
from nutrition.models import Nutrition, Plan
import json
from datetime import datetime, time
import math
from posts.models import Post
from activities.models import Comment
from groups.models import Group,GroupMember
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
#Django Auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView


def signup(request):
    """
    Sign up page
    :param request:
    :return to Homepage
    """

    if request.method == 'POST':
        form =  UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form =  UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    '''return user progile page'''
    args = {'user' : request.user }
    return render(request, 'accounts/profile.html', args)


#Friends List
def get_users(request):
    users = User.objects.all()
    return render (request, 'accounts/users.html', {'users':users})

#edit user profile
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


def filter(request):
    """
    get input from the user and return the output
    :param request: data
    :return: date
    """
    if request.method == 'POST':
        form = FilterDate(request.POST, instance=request.user.userprofileinfo)
        if form.is_valid():
            date = form.cleaned_data.get('timestamp')

    elif request.GET.get('year'):
        date = (request.GET.get('year'))

    else:
        date = datetime.datetime.now()

    return date

def manager_control(request):
    """
    get the manage control page for the adminstrator
    :param request: WSGIReques
    :return: render
    """
    if request.user.is_superuser:

        users = User.objects.all()
        return render(request, 'accounts/manager_control.html', {'users': users})


#Dashboard Admin
def visual_manage_control(request):
    if request.user.is_superuser:
        date = filter (request)
        dataSource = list_of_activity_log(date)
        content7 = activity_log_all(request, dataSource)
        data = return_list_of_WeightLossPercentage()

        #Return statistics values
        num = []
        for user in User.objects.all():
            num.append(calc_total_loss_per(user, user.userprofileinfo.current_weight))
        num = numbers(num)
        content4 = WeightLossPercentage(request, data)
        content5 = weight_lossDistrbotion(request)
        content8 = activity_log_by_type(request)
        return render(request, 'accounts/manage_graph.html',
                      {'output4': content4, 'output5': content5, 'output7': content7, 'output8': content8, 'numbers':num})



def list_of_activity_log(date):
    """
    Get the activity log of all the users
    :param date:
    :return: dict
    """
    dataSource = {}
    dataSource['data'] = []

    if isinstance(date, str):
        for user in User.objects.all():
                data = {}
                data['label'] = user.username
                data['value'] = Post.objects.filter(user=user, created_at__year=date).count() + \
                                Post.objects.filter(likes=user, date_of_like__year=date).count() + \
                                Comment.objects.filter(user=user, timestamp__year=date).count() + \
                                GroupMember.objects.filter(user=user, date__year=date).count()
                dataSource['data'].append(data)
    else:
        for user in User.objects.all():
            month = myconverter_month(date)
            year = myconverter_year(date)
            data = {}
            data['label'] = user.username
            data['value'] = Post.objects.filter(user=user, created_at__month=month,
                                                created_at__year=year).count() + \
                            Post.objects.filter(likes=user, date_of_like__month=month,
                                                date_of_like__year=year).count() + \
                            Comment.objects.filter(user=user, timestamp__month=month,
                                                   timestamp__year=year).count() + \
                            GroupMember.objects.filter(user=user, date__month=month,
                                                       date__year=year).count()
            dataSource['data'].append(data)
    return dataSource



def list_of_weight_loss(date, user):

    if isinstance(date, str):
        list = user.userprofileinfo.weight_history.filter(timestamp__year=date)
    else:
        month = myconverter_month(date)
        year = myconverter_year(date)
        list = user.userprofileinfo.weight_history.filter(timestamp__year=year, timestamp__month=month)
    return list;


def chart_user(request, username):
    """
    render all the graphs of the user, in the user profile page
    :param request:
    :param username:
    :return:
    """
    if request.user.username == username or request.user.is_superuser:
        date = filter(request)
        user = User.objects.get(username=username)
        if isinstance(date, str):
            plans = Plan.objects.filter(user=user, date__year=date)
        else:
            month = myconverter_month(date)
            year = myconverter_year(date)
            plans = Plan.objects.filter(user=user, date__month=month, date__year=year)

        list = list_of_weight_loss(date, user)
        content1 = chart(request, list)
        content2 = chart_bodyfat(request, list)
        content3 = chart_calories(request, plans)
        content5=weight_lossDistrbotion(request)
        content6=activity_log_chart(request, username)
        value = calc_total_loss_per(user, user.userprofileinfo.current_weight)

        return render(request, 'accounts/Graph.html',
                      {"user": user, 'output': content1, 'output2': content2, 'output3': content3,
                        'output5': content5, 'output6': content6, 'output6': content6, 'value':value})

    else:
        return HttpResponseRedirect(reverse("accounts:profile", kwargs={"username": request.user.username}))

def calc_bmi(user_P):
    """calculate bmi
    cal
    :param user_P:
    :return: int
    """
    if (user_P.height is None or user_P.current_weight is None):
        bmi = "Empty"
    else:
        bmi = round((user_P.current_weight) / (user_P.height) ** 2, 2)
    return bmi

#perosonal profile
@login_required
def personal_profile(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        bmi = calc_bmi(user_P)
        return render(request, 'accounts/personal_profile.html', {"user":user, 'bmi': bmi })
    else:
        return HttpResponse("No access to this page")

#profile
@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        user_P = UserProfileInfo.objects.get(user=user)
        my_groups = GroupMember.objects.filter(user=user)
        my_post  = Post.objects.filter(user=user)
        url = reverse("posts:for_user",  kwargs={"username": user.username})
        return render(request, 'accounts/profile.html', {"user":user, 'my_groups': my_groups, 'url':url, 'my_post':my_post  })



@login_required
#edit
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

#delete
def delete_weight(request, pk, username):
    user = User.objects.get(username=username)
    user_P = UserProfileInfo.objects.get(user=user)
    d= WeightList.objects.get(id=pk)
    d.delete()
    return HttpResponseRedirect(reverse("accounts:personal_profile", kwargs={"username": user.username }))


#Adding a new weighing
def add_weight(request, username):
    if request.user.is_superuser or request.user.username == username:
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

#
def get_groups(request, username):
    """
    :param request:
    :param username:
    :return: HttpResponse - get all the groups the user is following
    """
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
#chart of wieght loss
def chart(request, list):
    """
    :param request:
    :param list:
    :return: Chart of wieght loss for an individual user
    """
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


#Chart of body fat loss for an individual user
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


#Chart of calories intake for an individual user
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


def return_list_of_WeightLossPercentage():
    dataSource = {}
    dataSource['data'] = []
    for user in User.objects.all():
        data = {}
        data['label'] = user.username
        data['value'] = calc_total_loss_per(user, user.userprofileinfo.current_weight)
        dataSource['data'].append(data)
    return dataSource




#Calculate the percentage of weight loss for each user and return the graph with results
def WeightLossPercentage(request, dataSource):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource['chart'] = {
        "caption": "Weight loss Percentage",
        "subCaption": "Weight loss Percentage",
        "yAxisName": "Weight loss Percentage",
        "numberPrefix": "%",
        "setadaptiveymin": "1",
        "theme": "fint",
        "palettecolors": "#FF2DC6,#632289,#FFAE00,#D208F7,#6D08F7",
    }
    column2D = FusionCharts("column2d", "ex4", "600", "350", "chart-4", "json", dataSource)
    return (column2D.render())

#Distribution of percent weight loss for all users
def weight_lossDistrbotion(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = { }
    dataSource['chart'] = {
        "caption": "Weight loss distribution for now  ",
        "subCaption": "Weight loss of all the users in %",
        "bgColor": "#FFFFFF",
        "theme": "fint",
        "valueFontSize": "15",
        "palettecolors": "#0075c2",
    }
    #ranges of the distrbution
    labels = ["0","1-9", "10-19", "20-29", "30-39", "40-49", "50"]
    negatives =  ["0","-1--9","-10-19","-20--29","-30-39","-40--49","-50"]
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.

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

# chart activity-log of Individual user
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
        "palettecolors": "#0075c2,#FC4242, #0075c2,#06AF8F ",
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

#chart avtivity-log of all the users
def activity_log_all(request, dataSource):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.

    dataSource['chart'] = {
        "caption": "Activity Log",
        "subCaption": "Posts, comments, group follows and likes distribution",
        "xAxisName": "Month",
        "theme": "fint",
        "valueFontSize": "15",
        "showlegend": "1",
        "legendposition": "bottom",
    }
    column2D = FusionCharts("pie2d", "ex7", "600", "450", "chart-7", "json", dataSource)
    return (column2D.render())


def activity_log_by_type(request):
    '''return chart of numbes of activies by type'''
    dataSource = {}
    dataSource['chart'] = {
         "caption": "Activity Distribution by type",
         "subcaption": "For all users in 2018",

        "defaultcenterlabel": "Social app Distribution",
        "aligncaptionwithcanvas": "0",
        "captionpadding": "0",
        "decimals": "1",
        "theme": "fint",
        "valueFontSize": "15",

    }

    dataSource['data'] = []
    lables = ["post", "Comments", "Groups", "likes"]
    values = [Post.objects.all().count(), Comment.objects.all().count(), Group.objects.all().count(),Post.calculate_likes2()]
    for i in range(lables.__len__()):
        data = {}
        data['label'] = lables[i]
        data['value'] = values[i]
        dataSource['data'].append(data)

    column2D = FusionCharts("doughnut2d", "ex8", "600", "450", "chart-8", "json", dataSource)
    return (column2D.render())


from accounts.printing import MyPrint
from io import BytesIO

#export report of users names
def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_users()

    response.write(pdf)
    return response
#Total weight loss in KG
def calc_total_loss(user, current):
    total = 0
    for key in user.userprofileinfo.weight_history.all():
        if total == 0:
           total = current - key.weight
        else:
           break
        break
    return total
#Calculation of weight loss percentages
def calc_total_loss_per(user, current):
    total = 0
    for k in user.userprofileinfo.weight_history.all():
        if total == 0:
           total = round((((k.weight- current)/k.weight)*100),2)
        else:
           break
        break
    return total


# Reports
from django.http import HttpResponse
from django.views.generic import View
from accounts.printing import render_to_pdf #created in step 4

#Reports page
def generate_reports(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/reports.html', {'user':user })

#admin report page
def generate_reports_admin(request):
    GeneratePdf_of_all_user(request)
    return render(request, 'accounts/admin_reports.html')


import numpy as np
from statistics import mean, stdev, median
from decimal import Decimal as d


#Calc Wieght Loss statistics
def numbers(numbers1):
    avg = round((mean(numbers1)), 2)
    std = round(stdev(numbers1), 2)
    med = round(median(numbers1), 2)
    numbers1 = {'avg': avg, 'std': std, 'med': med, 'max':max(numbers1), 'min':  min(numbers1) }
    return numbers1

#progress report of all users: total  weight loss in kg and percentages
def GeneratePdf_of_all_user(request):
    if request.user.is_superuser:
        dataSource = {}
        dataSource['data'] = []
        numbers1 = []
        numbers2 = []
        for user in User.objects.all():
                data = {}
                data['weight_loss_per'] = calc_total_loss_per(user, user.userprofileinfo.current_weight)
                data['weight_loss']  = calc_total_loss(user, user.userprofileinfo.current_weight)
                data ['user'] = user
                numbers1.append(data['weight_loss_per'])
                numbers2.append(data['weight_loss'])
                dataSource['data'].append(data)

        numbers1 = numbers(numbers1)
        numbers2 = numbers(numbers2)

        pdf = render_to_pdf('accounts/all_users_report.html',
                            {'data': dataSource, 'numbers1': numbers1, 'numbers2': numbers2})

        return HttpResponse(pdf, content_type='application/pdf')

    else:
        return render(request, 'accounts/reports.html')
import datetime
#progress report of one user + filter by month & year
def  GeneratePdf(request, username):
        user = User.objects.get(username=username)
        dataSource = {}
        dataSource['data'] = []
        date = filter(request)

        list = list_of_weight_loss(date, user)
        for k in list:
                data = {}
                data['body_fat']= k.body_fat
                data['weight'] = k.weight
                data['timestamp'] = k.timestamp
                current = k.weight
                dataSource['data'].append(data)
        if (isinstance(date, datetime.date)):
            year = myconverter_year(date)
            type = date.strftime('%B') + " " + year
        else:
            type =date
        total = calc_total_loss(user, current)
        total_in_per = calc_total_loss_per(user, current)
        bmi = calc_bmi(user.userprofileinfo)
        pdf = render_to_pdf('accounts/pdf_template.html',
                                        {'data': dataSource, 'total': total, 'total_in_per': total_in_per,
                                         'bmi': bmi, 'user': user, 'type': type })

        return HttpResponse(pdf, content_type='application/pdf')

#Activity log report of all the users
def ActivityLogReport(request):
    if request.user.is_superuser:
        dataSource = {}
        numbers= []
        dataSource['data'] = []
        if request.method == "POST":
            form = FilterDate(request.POST, instance=request.user.userprofileinfo)
            if form.is_valid():
                time = form.cleaned_data.get('timestamp')
                month = myconverter_month(time)
                year = myconverter_year(time)
                type = time.strftime('%B') + " " + year
                for user in User.objects.all():
                    data = {}
                    data['label'] = user
                    data['post'] = Post.objects.filter(user=user, created_at__month=month, created_at__year=year).count()
                    data ['like'] = Post.objects.filter(likes=user, date_of_like__month=month, date_of_like__year=year).count()
                    data['follow'] = GroupMember.objects.filter(user=user, date__month=month, date__year=year).count()
                    data['comment'] =  Comment.objects.filter(user=user, timestamp__month=month, timestamp__year=year).count()
                    data['value'] = data['post'] + data['like'] + data['comment'] + data['follow']
                    dataSource['data'].append(data)
                    numbers.append(data['value'])

            avg = round(mean(numbers), 2)
            pdf = render_to_pdf('accounts/Activity_log_report.html', {'data': dataSource, 'avg' : avg, 'type': type})

            return HttpResponse(pdf, content_type='application/pdf')

