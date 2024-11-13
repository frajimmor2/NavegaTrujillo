from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator
#Todo ok
# Create your models here.

class Port(models.Model):
    ubication = models.CharField(max_length=150,validators=[MinLengthValidator(0)])

    def __str__(self):
        return f"{self.ubication}"

class Ship(models.Model):
    port = models.ForeignKey(Port,on_delete=models.CASCADE)

    capacity = models.IntegerField(default=2, validators=[MinValueValidator(2)])
    rent_per_day = models.FloatField(default=0., validators=[MinValueValidator(0.)])
    available = models.BooleanField(default=True)
    need_license = models.BooleanField()
    description = models.CharField(max_length=350,validators=[MinLengthValidator(0)])
    image = models.ImageField()
    name = models.CharField(max_length=45,unique=True, validators=[MinLengthValidator(0)])

    def __str__(self):
        return f"{self.name} - {self.capacity} {self.rent_per_day} {self.available} {self.need_license} {self.description}"

class Shopping_basket(models.Model):
    ships = models.ManyToManyField(Ship)

    rental_start_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    rental_end_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    captain_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.rental_start_date} {self.rental_end_date} {self.captain_amount}"


class Reservation_state(models.TextChoices):
    RESERVED = 'R', 'RESERVED'
    RESERVED_AND_PAID = 'P', 'RESERVED_AND_PAID'
    CANCELED = 'C', 'CANCELED'
    ALREADY_RENTED = 'A', 'ALREADY_RENTED'

class Reservation(models.Model):
    ships = models.ManyToManyField(Ship)
    port = models.OneToOneField(Port, on_delete=models.CASCADE)

    rental_start_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    rental_end_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    captain_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_cost = models.FloatField(validators=[MinValueValidator(0.)])
    reservation_state = models.CharField(
        max_length=1,
        choices=Reservation_state.choices,
        default=Reservation_state.RESERVED,
    )

    def __str__(self):
        return f"{self.rental_start_date} {self.rental_end_date} {self.captain_amount} {self.total_cost} {self.reservation_state}"

