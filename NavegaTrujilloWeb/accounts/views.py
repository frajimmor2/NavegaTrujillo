from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate 
from .forms import CustomUserCreationForm,LoginForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

class LoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy("home")
    template_name = "registration/login.html"
