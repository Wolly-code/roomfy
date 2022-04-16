from unicodedata import name
from django.urls import path, include
from . import views
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('signup', views.signup),
    path('login', views.login),
    path('profile', views.ViewProfile.as_view()),
    path('profile/<int:pk>', views.UpdateProfile.as_view()),
    path('profile/all',views.ViewAllProfile.as_view()),
]
