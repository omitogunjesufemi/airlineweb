from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Aircraft(models.Model):
    aircraft_name = models.CharField(max_length=20)
    aircraft_type = models.CharField(max_length=20)
    aircraft_no = models.CharField(max_length=15)
    aircraft_capacity = models.IntegerField(max_length=None)
    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    def __str__(self):
        return f'Aircraft - {self.aircraft_name:15}{self.aircraft_no}'


class Flight(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.RESTRICT)
    flight_number = models.CharField(max_length=10)
    take_off_location = models.CharField(max_length=50)
    price = models.FloatField()
    arrival_time = models.TimeField()
    destination = models.CharField(max_length=50)
    departure_date = models.DateField()
    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    def __str__(self):
        return f'{self.aircraft_id:25} {self.flight_number:25} {self.take_off_location:40} {self.price:25}\
        {self.departure_date:25} {self.destination:25} {self.arrival_time:25} {self.date_created:25}\
         {self.date_updated:25}'


class Passenger(models.Model):
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    registration_number = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name:25} {self.last_name:25} {self.email:25} {self.phone:25} {self.address:25}\
        {self.registration_number:25}'


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.RESTRICT)
    passenger = models.ForeignKey(Passenger, on_delete=models.RESTRICT)
    booking_reference = models.CharField(max_length=10)
    flight_class = models.CharField(max_length=20)
    seat_number = models.IntegerField(max_length=None, null=False)
    price = models.FloatField()

    def __str__(self):
        return f'{self.flight:25} {self.passenger:25} {self.booking_reference:25} {self.flight_class:25}\
        {self.price:25}'


class Staff(models.Model):
    date_of_employment = models.DateField(null=True)
    role = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
