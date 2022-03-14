import datetime
from typing import final
from Room.models import  Booking_Room
from Tenant.models import Appointment
from datetime import timedelta

def check_availability_room(room, check_in, check_out):
    avail_list = []
    Booking_list = Booking_Room.objects.filter(room=room)
    for booking in Booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)


# def check_availability_tenant(tenant, appoint):
#     final_date=appoint.today()+timedelta(days=1)
#     print(final_date)
#     avail_list = []
#     Appointment_list = Appointment.objects.filter(tenant=tenant)
#     for appointment in Appointment_list:
#         if appointment.appointment_date>final_date or final_date<appointment.appointment_date:
#             avail_list.append(True)
#         else:
#             avail_list.append(False)
#     return all(avail_list)
