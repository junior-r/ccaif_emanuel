from django.contrib import admin
from Posts.models import Event
from Posts.forms import EventForm


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', 'created_at', 'active']
    form = EventForm


admin.site.register(Event, EventAdmin)
