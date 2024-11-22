from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as LoginView_Django
from django.shortcuts import render,redirect
from business.models import Shopping_basket
from .models import Client 
from django.contrib.auth import login, authenticate 
from .forms import CustomUserCreationForm,LoginForm


class SignUpView(CreateView):
    
    ''' Registro, crea el usuario (si los datos son correctos, de eso se encarga Django) y les asigna un cliente y una cesta de la compra'''

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
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


class LoginView(LoginView_Django):
    ''' Login básico, la chicha está en el frontend y en el formulario '''
    form_class = LoginForm
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("home")



class FastLoginView(LoginView_Django):
    ''' Login para compra rápida, redirige a un lugar diferente '''
    form_class = LoginForm
    template_name = "registration/login.html"
    
    def get_success_url(self):
        # Magia negra chaval
        return reverse_lazy("reservation_dates",kwargs={'ship_id':self.kwargs['ship_id']})




