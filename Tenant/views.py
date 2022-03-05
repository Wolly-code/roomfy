from django.shortcuts import render
from rest_framework import generics, status, permissions, mixins

from Room import serializers
from .models import Report_Tenant, Tenant
from .serializers import TenantSerializer,ReportTenant
from rest_framework.exceptions import ValidationError

# Create your views here.


class TenantList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class TenantRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def delete(self, request, *args, **kwargs):
        post = Tenant.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Thats not your post to delete')

    def perform_update(self, serializer):
        serializer.save()

class TenantReportCreate(generics.CreateAPIView):
    serializer_class = ReportTenant
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        user = self.request.user
        post = Tenant.objects.get(pk=self.kwargs['pk'])
        return Report_Tenant.objects.filter(Reporter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already reported for this post')
        serializer.save(Reporter=self.request.user,
                        post=Tenant.objects.get(pk=self.kwargs['pk']))

class ViewAllReport(generics.ListAPIView):
    serializer_class=ReportTenant
    permissions=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Report_Tenant.objects.all()