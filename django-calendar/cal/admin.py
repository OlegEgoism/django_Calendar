from django.contrib import admin
from .models import Event, User


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = 'user', 'title', 'short_description', 'start_time', 'end_time', 'date_create',
    list_filter = 'start_time', 'end_time', 'date_create',

    def short_description(self, obj):
        if len(obj.description) > 200:
            return obj.description[:200] + "..."
        else:
            return obj.description

    short_description.short_description = 'Описание'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'name', 'color', 'count_user_event',
    list_editable = 'color',
