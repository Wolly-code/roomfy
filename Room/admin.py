from django.contrib import admin
from .models import Favorite, Room, Booking_Room, Payment_Room, Report_Room
# Register your models here.

admin.site.register(Room)
admin.site.register(Booking_Room)
admin.site.register(Payment_Room)
admin.site.register(Report_Room)
admin.site.register(Favorite)
