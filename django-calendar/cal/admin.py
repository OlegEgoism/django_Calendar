from django.contrib import admin
from .models import Event, User


# Register your models here.
# admin.site.register(Event)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = 'title', 'description', 'start_time'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'name',
