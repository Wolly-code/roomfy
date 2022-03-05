import datetime
from Room.models import Room, Booking_Room


def check_availability_room(room, check_in, check_out):
    avail_list = []
    Booking_list = Booking_Room.objects.filter(room=room)
    for booking in Booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
