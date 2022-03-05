from unicodedata import name
from django.urls import path, include
from . import views
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('signup', views.signup),
    path('login', views.login),
]
