from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tenant(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15)
    occupation = models.CharField(max_length=20)
    age = models.IntegerField()
    pet_owner = models.BooleanField()
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    Budget = models.IntegerField()
    Preference = models.CharField(max_length=25)
    Title = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    photo1 = models.ImageField(upload_to="tenant", blank=True)
  

    class Meta:
        # This helps to order the data in the admin portion
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.full_name}'


class Report_Tenant(models.Model):
    Reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default="Scam")

    def __str__(self) -> str:
        return f'{self.post} having complain "{self.description}"-{self.Reporter}'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user} has booked appointment on {self.Tenant} on the date :{self.appointment_date}'


class Payment_Tenant(models.Model):
    Payment_ID = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    Amount = models.IntegerField()
    Payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} has paid the amount of {self.Amount} {self.Payment_date}'
