from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Room(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=30)
    total_rooms = models.IntegerField()
    price = models.IntegerField()
    security_deposit=models.IntegerField()
    internet = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    Balcony = models.BooleanField(default=False)
    Yard = models.BooleanField(default=False)
    Disabled_Access = models.BooleanField(default=False)
    Garage = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    photo1 = models.ImageField(upload_to="room", blank=True)
    photo2 = models.ImageField(upload_to="room", blank=True)

    class Meta:
        # This helps to order the data in the admin portion
        ordering = ['-created']

    def __str__(self):
        return self.title 


class Report_Room(models.Model):
    Reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default="Scam")

    def __str__(self) -> str:
        return f'{self.post} having complain "{self.description}"-{self.Reporter}'


class Booking_Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'


class Payment_Room(models.Model):
    Payment_ID = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Amount = models.IntegerField()
    Payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} has paid the amount of {self.Amount} {self.Payment_date}'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"Room={self .room} || User={self.user.username} || Favourite={self.favourite}"
