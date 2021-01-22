from django.contrib import admin
from .models import UserType, Event, Address, event_photo


class EventAdmin(admin.ModelAdmin):
    list_display = ("id","service", "Max_Guest", "start_date", "end_date","payment_status","user_event_request")
    list_filter = ("service", "Max_Guest", "start_date", "end_date")
    search_fields = ("service", "Max_Guest", "start_date", "end_date")


class AddressAdmin(admin.ModelAdmin):
    list_display = ("city", "address", "country", "pincode")
    list_filter = ("city", "address", "country", "pincode")
    search_fields = ("city", "address", "country", "pincode")


class Event_photo_admin(admin.ModelAdmin):
    list_display = ("event")


admin.site.register(UserType)
admin.site.register(Event, EventAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(event_photo)
