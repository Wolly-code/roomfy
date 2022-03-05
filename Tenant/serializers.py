from rest_framework import serializers
from .models import Report_Tenant, Tenant
from django.contrib.auth.models import User


class TenantSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    reports = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = ['id', 'full_name', 'poster', 'gender',
                  'reports', 'phone_number', 'occupation', 'age', 'pet_owner', 'location',
                  'Budget', 'Preference', 'Title', 'description', 'created', 'status']

    def get_reports(self, post):
        return Report_Tenant.objects.filter(post=post).count()


class ReportTenant(serializers.ModelSerializer):
    class Meta:
        model = Report_Tenant
        fields = ['id','post', 'description']
