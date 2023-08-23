from django.contrib import admin
from .models import Event, User


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = 'user', 'title', 'description', 'start_time', 'end_time',
    list_filter = 'start_time', 'end_time',


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'name', 'count_user_event',
