from django.contrib import admin

from .models import Category, Area, Event, User

class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'host', 'date']

admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Area)
admin.site.register(User)