from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('home/cart/', views.cart, name="cart"),
    path('reserva/<int:ship_id>', views.reservation, name="reservation"),
]
