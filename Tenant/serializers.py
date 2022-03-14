from rest_framework import serializers
from .models import Appointment, Report_Tenant, Tenant
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
        fields = ['id', 'post', 'description']


class AppointmentSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Appointment
        fields = '__all__'
