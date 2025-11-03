from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pickup = models.CharField(max_length=255,null=True, blank=True)
    drop = models.CharField(max_length=255 ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15 ,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.CharField(max_length=15, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    fare = models.CharField(max_length=100, null=True, blank=True)
    drive = models.CharField(max_length=100, null=True, blank=True)
    total = models.CharField(max_length=100, null=True, blank=True)
    driverCharge = models.CharField(max_length=100, null=True, blank=True)
    carType = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending') 
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class sedancar(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=5, null=True, blank=True)
   

    def __str__(self):
        return self.name
    
class RoundTrip(models.Model):
    round = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pickup = models.CharField(max_length=255,null=True, blank=True)
    drop = models.CharField(max_length=255 ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15 ,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.CharField(max_length=15, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    number_of_days = models.IntegerField()
    distance = models.FloatField(null=True, blank=True)
    fare = models.CharField(max_length=100, null=True, blank=True)
    total = models.CharField(max_length=100, null=True, blank=True)
    driverCharge = models.CharField(max_length=100, null=True, blank=True)
    carType = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending') 
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
