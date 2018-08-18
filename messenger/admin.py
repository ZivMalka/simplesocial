from django.contrib import admin
from messenger.models import Message
# Register your models here.
#admin.site.register(models.Message)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp")
    list_filter = ("sender", "recipient")