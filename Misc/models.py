from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self) -> str:
        return self.user.username

