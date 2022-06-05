from rest_framework import serializers
from .models import Favourite, Report_Room, Room, Booking_Room, Payment_Room
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    reports = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_reports(self, post):
        return Report_Room.objects.filter(post=post).count()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report_Room
        fields = ['id', 'description']


class PaymentSerializer(serializers.ModelSerializer):
    room_owner = serializers.ReadOnlyField(source='room.poster.username')
    user=serializers.ReadOnlyField(source='user.username')
    # room=serializers.SerializerMethodField()
    class Meta:
        model = Payment_Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    room_owner = serializers.ReadOnlyField(source='room.poster.username')
    room=serializers.ReadOnlyField(source='room.id')
    class Meta:
        model = Booking_Room
        fields = '__all__'


class FavouriteSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Favourite
        fields = ('id', 'favourite', 'room', 'user')
        # fields="__all__"
