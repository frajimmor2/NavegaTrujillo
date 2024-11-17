from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    
    name = models.CharField(max_length=50,validators=[MinLengthValidator(0)], blank=False)
    surname = models.CharField(max_length=100,validators=[MinLengthValidator(0)], blank=False)
    email = models.CharField(max_length=50,validators=[MinLengthValidator(0)], blank=False)

    def __str__(self):
        return f"{self.name} {self.surname} : {self.email}"


