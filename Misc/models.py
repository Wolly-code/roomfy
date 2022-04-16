from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    email=models.EmailField()
    profile_pic=models.ImageField(upload_to="user")
    location=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)


    def __str__(self) -> str:
        return self.user.username

