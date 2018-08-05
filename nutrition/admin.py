from django.contrib import admin
from . import models

class PlanAdmin(admin.ModelAdmin):
      list_display = ('subtitle', 'user', 'date')
      list_filter = ('user', 'date')
      search_fields = ('subtitle',)

class NutritionAdmin(admin.ModelAdmin):
    list_display = ('time', 'energy')

admin.site.register(models.Plan, PlanAdmin)
admin.site.register(models.Nutrition, NutritionAdmin)