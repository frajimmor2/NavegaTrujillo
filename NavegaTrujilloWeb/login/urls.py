from django.contrib import admin
from django.urls import path, include

from login.views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
]
