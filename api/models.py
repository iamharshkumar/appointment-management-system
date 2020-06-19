from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_status(models.Model):
    status = models.CharField(max_length=100, null=True, default="pending")

    def __str__(self):
        return self.status


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(User_status, on_delete=models.CASCADE, null=True, default=1)
    mobile = models.IntegerField(null=True)
    id_card_no = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Service(models.Model):
    name = models.CharField(max_length=100, null=True)
    cost = models.IntegerField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.name


class Book_status(models.Model):
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.status


class Booking_Paid(models.Model):
    paid = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.paid


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Book_status, on_delete=models.CASCADE, null=True)
    paid = models.ForeignKey(Booking_Paid, on_delete=models.CASCADE, null=True)
    date1 = models.DateField(null=True)
    time1 = models.DateField(null=True)

    def __str__(self):
        return self.customer.user.username + "" + self.service.name
