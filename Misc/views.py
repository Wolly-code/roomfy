from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.http import  JsonResponse
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.contrib.auth.models import User

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
