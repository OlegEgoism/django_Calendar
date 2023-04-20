from django.contrib import admin
from cal.models import Event

# Register your models here.
# admin.site.register(Event)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
   list_display = 'id', 'title', 'description'