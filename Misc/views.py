from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import generics, permissions, mixins
from rest_framework.exceptions import ValidationError
from Misc.models import Profile
from Misc.serializers import ProfileSerializers

# Create your views here.


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error': 'Couldnot login Please Check user name and password bozo'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token), 'username': data['username']}, status=200)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token), 'username': data['username']}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'That username has already been taken. Please choose a new username'}, status=400)


class ViewProfile(generics.ListCreateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateProfile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializers

    def perform_update(self, serializer):
        return serializer.save()

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)
    def delete(self, request, *args, **kwargs):
        user = Profile.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if user.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Thats not your post to delete')
