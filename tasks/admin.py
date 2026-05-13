from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Task


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'completed',
        'created_at'
    )