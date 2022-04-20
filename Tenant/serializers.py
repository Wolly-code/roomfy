from rest_framework import serializers
from .models import Appointment, Report_Tenant, Tenant, Tenant_Favourite
from django.contrib.auth.models import User


class TenantSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    reports = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = '__all__'

    def get_reports(self, post):
        return Report_Tenant.objects.filter(post=post).count()


class ReportTenant(serializers.ModelSerializer):
    class Meta:
        model = Report_Tenant
        fields = ['id', 'description']

class TenantFavorites(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Tenant_Favourite
        fields = ('id', 'favourite', 'tenant', 'user')
        # fields="__all__"


class AppointmentSerializer(serializers.ModelSerializer):   
    user=serializers.ReadOnlyField(source='user.username')
    tenant_poster=serializers.ReadOnlyField(source='Tenant.poster.username')
    class Meta:
        model = Appointment
        fields = '__all__'
