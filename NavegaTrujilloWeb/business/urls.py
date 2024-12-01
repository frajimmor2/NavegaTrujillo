from django.urls import path,include

from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path('reserva/<int:ship_id>', views.reservation, name="reservation_dates"),
    path('reserva/<int:ship_id>/confirmacion', views.confirm_reservation, name="confirm_reservation"),
    path('paypal/<int:ship_id>/confirmacion/<int:captain>', views.confirm_reservation_paypal, name="confirm_reservation_paypal"),
    path('cart/', views.cart, name="cart"),
    path('cart/reserva', views.cart_reservation, name = "cart_reservation"),
    path('cart/reserva/confirmacion', views.confirm_reservation_cart, name = "cart_reservation_confirm"),
    path('add-port/', views.add_port, name="add_port"),
    #path('paypal_confirm',views.paypal_congrats,name="paypal_congrats"),
]
