from asyncio import mixins
from distutils.log import error
from telnetlib import STATUS
from django.http import HttpResponse
from rest_framework import generics, permissions, mixins, serializers
from .models import Favourite, Report_Room, Room, Booking_Room
from .serializers import ReportSerializer, BookingSerializer, RoomSerializer, FavouriteSerializers
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

    # def delete(self, request, *args, **kwargs):
    #     if self.get_queryset().exists():
    #         self.get_queryset().delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         raise ValidationError('You never reported for this post')


class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking_Room.objects.all()
        elif self.request.user.is_authenticated:
            return Booking_Room.objects.filter(user=self.request.user)
        elif self.request.user.is_anonymous:
            return Booking_Room.objects.none()

    def perform_create(self, serializer):
        if not self.request.user:
            return ValidationError("Please log in to continue")
        available_rooms = []
        room_list = Room.objects.all()
        for room in room_list:
            if check_availability_room(room, check_in=serializer.validated_data['check_in'], check_out=serializer.validated_data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            serializer.save(user=self.request.user, room=room)
        else:
            raise ValidationError('This room is not available')


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
