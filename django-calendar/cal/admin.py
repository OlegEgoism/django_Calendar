from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from .models import Event, User


class UserFilter(AutocompleteFilter):
    title = 'Пользователь'
    field_name = 'user'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = 'user', 'title', 'short_description', 'start_time', 'end_time', 'date_create',
    list_filter = UserFilter, ("start_time", DateRangeFilterBuilder()), ("end_time", DateRangeFilterBuilder()), \
        ("date_create", DateRangeFilterBuilder()),
    search_fields = 'title', 'description',
    search_help_text = 'Поиск по заголовку и описанию'
    list_per_page = 20

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + "..."
        else:
            return obj.description

    short_description.short_description = 'Описание'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'name', 'color', 'count_user_event',
    list_editable = 'color',
    search_fields = 'name',
    search_help_text = 'Поиск ФИО'
    list_per_page = 20