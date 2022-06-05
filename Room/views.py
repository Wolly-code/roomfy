from asyncio import mixins
from distutils.log import error
from telnetlib import STATUS
from django.http import HttpResponse
from rest_framework import generics, permissions, mixins, serializers
from .models import Favourite, Payment_Room, Report_Room, Room, Booking_Room
from .serializers import PaymentSerializer, ReportSerializer, BookingSerializer, RoomSerializer, FavouriteSerializers
from rest_framework.exceptions import ValidationError
from Misc.booking_functions.availability import check_availability_room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import json


class RoomList(generics.ListCreateAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class SingleRoomView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(poster=user)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class RoomRetriveDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def delete(self, request, *args, **kwargs):
        post = Room.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Thats not your post to delete')

    def perform_update(self, serializer):
        serializer.save()


class ReportCreate(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        user = self.request.user
        post = Room.objects.get(pk=self.kwargs['pk'])
        return Report_Room.objects.filter(Reporter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already reported for this post')
        serializer.save(Reporter=self.request.user,
                        post=Room.objects.get(pk=self.kwargs['pk']))

from django.http import JsonResponse

class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        post = Room.objects.get(pk=self.kwargs['pk'])
        return Booking_Room.objects.filter(user=self.request.user, room=post)


    def perform_create(self, serializer):
        if not self.request.user:
            return ValidationError("Please log in to continue")
        available_rooms = []
        user_choice = Room.objects.get(pk=self.kwargs['pk'])
        if check_availability_room(user_choice, check_in=serializer.validated_data['check_in'], check_out=serializer.validated_data['check_out']):
                available_rooms.append(user_choice)

        if len(available_rooms) > 0:
            for each in available_rooms:
                if each == user_choice:
                    serializer.save(user=self.request.user, room=user_choice)
                    # return JsonResponse({'error': {'code':'BOOKING_EXISTS','message':'The room you are trying to book has already been booked by other user'}}, status=400)
                    # raise ValidationError('This room is not available')
        else:
            raise ValidationError('This room is not available')


class ViewAllBooking(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Booking_Room.objects.all()


class FavView(generics.ListAPIView):
    permissions = [permissions.IsAuthenticated]
    serializer_class = FavouriteSerializers

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)


class Fav(APIView):
    permissions = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # query = Favourite.objects.all()
            # serializer = FavouriteSerializers(query,many=True)
            data = request.data
            # data = request.data
            print(data)
            c_user = request.user
            room_id = data['id']
            room_obj = Room.objects.get(id=room_id)
            fav_obj = Favourite.objects.filter(
                room=room_obj).filter(user=c_user).first()
            if fav_obj:
                old_fav = fav_obj.favourite
                fav_obj.favourite = not old_fav
                fav_obj.save()
            else:
                Favourite.objects.create(
                    room=room_obj,
                    user=c_user,
                    favourite=True
                )
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class PaymentView(generics.ListCreateAPIView):
    permissions = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Payment_Room.objects.all()
