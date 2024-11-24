from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('reserva/<int:ship_id>', views.reservation, name="reservation_dates"),
    path('reserva/<int:ship_id>/confirmacion', views.confirm_reservation, name="confirm_reservation"),
    path('cart/', views.cart, name="cart"),
    path('cart/reserva', views.cart_reservation, name = "cart_reservation"),
    path('cart/reserva/confirmacion', views.confirm_reservation_cart, name = "cart_reservation_confirm"),
]
