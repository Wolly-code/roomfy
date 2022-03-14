from rest_framework import serializers
from .models import Favorite, Report_Room, Room, Booking_Room
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


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking_Room
        fields = ['id', 'user', 'room', 'check_in', 'check_out']


class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favorite
        fields = "__all__"
