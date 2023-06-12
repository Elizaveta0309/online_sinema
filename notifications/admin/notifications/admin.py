from django.contrib import admin

from .models import Config, ScheduleMail, Template


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):

    search_fields = ['name']


@admin.register(ScheduleMail)
class ScheduleMailAdmin(admin.ModelAdmin):

    search_fields = ['name']


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):

    search_fields = ['name']
