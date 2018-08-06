from django.shortcuts import render
from .forms import PlanForm, NutritionForm
from django.shortcuts import get_object_or_404
from django.views import generic
from nutrition.models import Plan, Nutrition
from django.db.models import Q
from django.template.context_processors import csrf
from django.views.generic import (
    UpdateView
)
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User

def create_plan(request):
    if request.user.is_superuser:
        form = PlanForm(request.POST or None)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return render(request, 'nutrition/detail.html', {'plan': plan})
        context = {
            "form": form,
        }
        return render(request, 'nutrition/create_plan.html', context)
    else:
        return HttpResponse("No access to this page")

def create_nutrition(request, plan_id):
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
                    return render(request, 'nutrition/create_nutrition.html', context)
            nutrition = form.save(commit=False)
            nutrition.plan = plan
            nutrition.save()
            return render(request, 'nutrition/detail.html', {'plan': plan})
        context = {
            'plan': plan,
            'form': form,
        }
        return render(request, 'nutrition/create_nutrition.html', context)


def delete_plan(request, plan_id):
    if request.user.is_superuser:
        plan = Plan.objects.get(pk=plan_id)
        plan.delete()
        plans = Plan.objects.filter(user=request.user)
        return render(request, 'nutrition/plan_list.html', {'plans': plans})


def delete_nutrition(request, plan_id, nutrition_id):
    if request.user.is_superuser:
        plan = get_object_or_404(Plan, pk=plan_id)
        nutrition = Nutrition.objects.get(pk=nutrition_id)
        nutrition.delete()
        return render(request, 'nutrition/detail.html', {'plan': plan})


def detail(request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        user = plan.user
        return render(request, 'nutrition/detail.html', {'plan': plan, 'user': user })


def plan_list(request, username):
    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        plans = Plan.objects.filter(user=user)
        nutrition_results = Nutrition.objects.all()
        query = request.GET.get("q")
        if query:
            plans = plans.filter(
                Q(plan_title__icontains=query) |
                Q(subtitle__icontains=query)
            ).distinct()
            nutrition_results = nutrition_results.filter(
                Q(nutrition_description__icontains=query)
            ).distinct()
            return render(request, 'nutrition/plan_list.html', {
                'plans': plans,
                'nutritions': nutrition_results,
            })
        else:
            return render(request, 'nutrition/plan_list.html', {'plans': plans})











