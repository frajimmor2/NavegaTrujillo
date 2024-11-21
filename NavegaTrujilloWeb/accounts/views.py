from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate

from business.models import Shopping_basket

from .models import Client 
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    
    ''' Registro, crea el usuario (si los datos son correctos, de eso se encarga Django) y les asigna un cliente y una cesta de la compra'''

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()

        shopping_basket = Shopping_basket.objects.create(
            rental_start_date=timezone.now().date(),
            rental_end_date=timezone.now().date(),
            captain_amount=0
        )

        client = Client.objects.create(
            shopping_basket=shopping_basket
        )

        user.client = client
        user.save()

        return super().form_valid(form)

