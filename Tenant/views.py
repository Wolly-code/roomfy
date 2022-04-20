from django.shortcuts import render
from rest_framework import generics, status, permissions, mixins
from Room import serializers
from .models import Appointment, Report_Tenant, Tenant, Tenant_Favourite
from .serializers import AppointmentSerializer, TenantFavorites, TenantSerializer, ReportTenant
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

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
    serializer_class = ReportTenant
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report_Tenant.objects.all()


class TenantAppointment(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.all()

    def perform_create(self, serializer):
        # available_appointment = []
        # tenant_list = Tenant.objects.all()

        # for tenant in tenant_list:
        #     if check_availability_tenant(tenant=tenant, appoint=serializer.validated_data['appointment_date']):
        #         available_appointment.append(tenant)

        # if len(available_appointment) > 0:
        #     tenant = available_appointment[0]
        #     serializer.save(user=self.request.user, Tenant=tenant)
        # else:
        #     raise ValidationError('You have already booked an appointment')
        serializer.save(user=self.request.user)


class FavView(generics.ListAPIView):
    permissions = [permissions.IsAuthenticated]
    serializer_class = TenantFavorites

    def get_queryset(self):
        return Tenant_Favourite.objects.filter(user=self.request.user)


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
            room_obj = Tenant.objects.get(id=room_id)
            fav_obj = Tenant_Favourite.objects.filter(
                tenant=room_obj).filter(user=c_user).first()
            if fav_obj:
                old_fav = fav_obj.favourite
                fav_obj.favourite = not old_fav
                fav_obj.save()
            else:
                Tenant_Favourite.objects.create(
                    tenant=room_obj,
                    user=c_user,
                    favourite=True
                )
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)