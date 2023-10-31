from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


admin.site.register(Task, TaskAdmin)
admin.site.register(User)
# Register your models here.
