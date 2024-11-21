from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate


from .models import Client, Shopping_basket 
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)

        shopping_basket = Shopping_basket.objects.create(
            rental_start_date=timezone.now().date(),
            rental_end_date=timezone.now().date(),
            captain_amount=0
        )

        client = Client.objects.create()

        user.shopping_basket = shopping_basket

        user.client = client
        user.save()

        return super().form_valid(form)

