from django.shortcuts import render
from .forms import PlanForm, NutritionForm
from django.shortcuts import get_object_or_404
from nutrition.models import Plan, Nutrition
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages


def create_plan(request):
    if request.user.is_superuser:
        form = PlanForm(request.POST or None)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            messages.success(request, 'Plan Added!')
            return render(request, 'nutrition/detail.html', {'plan': plan})
        context = {
            "form": form,
        }
        return render(request, 'nutrition/create_plan.html', context)
    else:
        return HttpResponse("Only authorized user can add nutrition meals")

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
            messages.success(request, 'Meal Added!')
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



def edit_meal(request,plan_id , nutrition_id):
    template = 'nutrition/edit_meal.html'
    plan = get_object_or_404(Plan, pk=plan_id)
    nutrition = get_object_or_404(Nutrition, pk=nutrition_id)
    if request.method == "POST":
        form = NutritionForm(request.POST, instance=nutrition)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Nutrition Has Been Updated')
                return render(request, 'nutrition/detail.html', {'plan': plan})
        except Exception as e:
            messages.warning(request, 'Your set was not saved due to an error: {}'.format(e))
    else:
        form = NutritionForm(instance=nutrition)
    context = {
        'form': form,
        'plan': plan,
    }
    return render(request, template, context)

def edit_plan(request, plan_id):
    template = 'nutrition/edit_plan.html'
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == "POST":
        form = PlanForm(request.POST, instance=plan)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Plan Has Been Updated')
                return render(request, 'nutrition/detail.html', {'plan': plan})
        except Exception as e:
            messages.warning(request, 'Your plan was not saved due to an error: {}'.format(e))
    else:
        form = PlanForm(instance=plan)
    context = {
        'form': form,
        'plan': plan,
    }
    return render(request, template, context)

def plan_list_manage(request, username):
    user = User.objects.get(username=username)
    plans = Plan.objects.filter(user=user)
    return render(request, 'nutrition/plan_list_manage.html', {'plans': plans})








