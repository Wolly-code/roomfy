from rest_framework import serializers
from Room.models import Room
from Tenant.models import Tenant
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    # rooms = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all())
    #  tenants = serializers.PrimaryKeyRelatedField(
    #      many=True, queryset=Tenant.objects.all())
    # owner = serializers.ReadOnlyField(source='owner.username')
    room = serializers.SerializerMethodField()

    def get_room(self, poster):
        return Room.objects.filter(poster=poster).count()

    class Meta:
        model = User
        # fields = ['id', 'username', 'rooms', 'owner']
        fields = ['id', 'username', 'room']


class ProfileSerializers(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Profile
        fields = '__all__'
