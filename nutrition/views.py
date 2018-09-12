from django.shortcuts import render, redirect
from .forms import PlanForm, NutritionForm
from django.shortcuts import get_object_or_404
from nutrition.models import Plan, Nutrition
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from notify.signals import notify
from django.http import HttpResponseRedirect
from django.urls import reverse


def create_plan(request, username):
    '''create new plan'''
    if request.user.is_superuser:
        form = PlanForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(username=username)
            subtitle = form.cleaned_data.get('subtitle')
            date = form.cleaned_data.get('date')
            plan = Plan.objects.create(user=user, subtitle=subtitle, date=date)
            messages.success(request, 'Plan Added!')
            notify.send(request.user, recipient=user, actor=request.user, verb='Added a new plan.',
                        nf_type='plan_by_one_user', target=plan)

            return render(request, "nutrition/detail.html", {'plan':plan})
        context = {
            "form": form,
        }

        return render(request, 'nutrition/create_plan.html', context)
    else:
        return HttpResponse("Only authorized user can add nutrition meals")


def create_nutrition(request, plan_id):
    '''create new nutrition'''
    if request.user.is_superuser:
        form = NutritionForm(request.POST or None)
        plan = get_object_or_404(Plan, pk=plan_id)
        if form.is_valid():
            plans_nutritions = plan.nutrition_set.all()
            for s in plans_nutritions:
                if s.description == form.cleaned_data.get("description"):
                    context = {
                        'plan': plan,
                        'form': form,
                        'error_message': 'You already added that description',
                    }
            nutrition = form.save(commit=False)
            nutrition.plan = plan
            nutrition.save()
            messages.success(request, 'Meal Added!')
            return HttpResponseRedirect(reverse("nutrition:detail", kwargs={"plan_id": plan.id}))

        context = {
            'plan': plan,
            'form': form,
        }
        return render(request, 'nutrition/create_nutrition.html', context)


def delete_plan(request, plan_id, username):
    """
    :param request:
    :param plan_id:
    :param username:
    delete
    """
    if request.user.is_superuser:
        plan = Plan.objects.get(pk=plan_id)
        plan.delete()
        return redirect('nutrition:plan_list_manage', username)


def delete_nutrition(request, plan_id, nutrition_id):
    """
    delete nutrition of a given user
    :param request:
    :param plan_id:
    :param nutrition_id:
    :return:
    """
    if request.user.is_superuser:
        plan = get_object_or_404(Plan, pk=plan_id)
        nutrition = Nutrition.objects.get(pk=nutrition_id)
        nutrition.delete()
        return render(request, 'nutrition/detail.html', {'plan': plan})


def detail(request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        user = plan.user
        return render(request, 'nutrition/detail.html', {'plan': plan, 'user': user })


from django.db.models import Q

def plan_list(request, username):
    '''plan list'''
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        if Plan.objects.filter(user=user):
            weekly = (Plan.objects.latest('date'))
            plans = Plan.objects.filter(Q(user=user) & ~Q(id=weekly.id))
        else:
            return render(request, 'nutrition/plan_list.html', {'user': user})
        return render(request, 'nutrition/plan_list.html', {'plans': plans, 'weekly':weekly, 'user': user})



def edit_meal(request,plan_id , nutrition_id, username):
    """
    :param request:
    :param plan_id:
    :param nutrition_id:
    :param username:
    :return:
    """
    plan = get_object_or_404(Plan, pk=plan_id)
    nutrition = get_object_or_404(Nutrition, pk=nutrition_id)
    if request.method == "POST":
        form = NutritionForm(request.POST, instance=nutrition)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Nutrition Has Been Updated')
                return render(request, 'nutrition/detail.html', {'plan': plan}, username)
        except Exception as e:
            messages.warning(request, 'Your set was not saved due to an error: {}'.format(e))
    else:
        form = NutritionForm(instance=nutrition)
    context = {
        'form': form,
        'plan': plan,
    }
    return render(request, 'nutrition/edit_meal.html', context)




def edit_plan(request, plan_id, username):
    """
    edit plan
    :param request:
    :param plan_id:
    :param username:
    :return:
    """
    plan = get_object_or_404(Plan, pk=plan_id)
    form = PlanForm(request.POST or None, instance=plan)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your Plan Has Been Updated')
        return redirect('nutrition:plan_list_manage', username)
    return render(request, 'nutrition/edit_plan.html', {'form':form})



def plan_list_manage(request, username):
    """
    return plan list in manage control
    :param request:
    :param username:
    :return:
    """
    user = User.objects.get(username=username)
    plans = Plan.objects.filter(user=user)
    return render(request, 'nutrition/plan_list_manage.html', {'plans': plans, 'user':user})








